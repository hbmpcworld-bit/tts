"""
Scheduler Module
Suggests optimal posting times and manages content scheduling
"""

from datetime import datetime, timedelta
import pytz
from utils.helpers import load_config, save_json, get_timestamp


class ContentScheduler:
    """Schedule TikTok posts for optimal engagement"""

    def __init__(self):
        self.config = load_config()
        self.scheduling_config = self.config.get('scheduling', {})
        self.timezone = pytz.timezone(self.scheduling_config.get('timezone', 'Asia/Karachi'))

    def get_best_times_today(self):
        """Get best posting times for today"""
        best_times = self.scheduling_config.get('best_times', ['09:00', '12:00', '18:00', '21:00'])

        today = datetime.now(self.timezone)
        posting_times = []

        for time_str in best_times:
            hour, minute = map(int, time_str.split(':'))
            post_time = today.replace(hour=hour, minute=minute, second=0, microsecond=0)

            # Only include future times
            if post_time > datetime.now(self.timezone):
                posting_times.append(post_time)

        return posting_times

    def create_schedule(self, video_count, days=7):
        """
        Create a posting schedule for multiple videos

        Args:
            video_count: Number of videos to schedule
            days: Number of days to spread posts over

        Returns:
            list: Schedule with dates and times
        """
        posts_per_day = self.scheduling_config.get('posts_per_day', 3)
        best_times = self.scheduling_config.get('best_times', ['09:00', '12:00', '18:00', '21:00'])

        schedule = []
        current_date = datetime.now(self.timezone).replace(hour=0, minute=0, second=0, microsecond=0)

        video_index = 0

        for day in range(days):
            if video_index >= video_count:
                break

            day_date = current_date + timedelta(days=day)

            # Determine how many posts for this day
            remaining_videos = video_count - video_index
            posts_today = min(posts_per_day, remaining_videos)

            # Select best times for this day
            times_today = best_times[:posts_today]

            for time_str in times_today:
                if video_index >= video_count:
                    break

                hour, minute = map(int, time_str.split(':'))
                post_datetime = day_date.replace(hour=hour, minute=minute)

                schedule.append({
                    'video_number': video_index + 1,
                    'datetime': post_datetime.isoformat(),
                    'date': post_datetime.strftime('%Y-%m-%d'),
                    'time': post_datetime.strftime('%H:%M'),
                    'day_of_week': post_datetime.strftime('%A'),
                    'timezone': str(self.timezone)
                })

                video_index += 1

        return schedule

    def get_next_best_time(self):
        """Get the next best posting time"""
        best_times = self.get_best_times_today()

        if best_times:
            return best_times[0]
        else:
            # If no more times today, get first time tomorrow
            tomorrow = datetime.now(self.timezone) + timedelta(days=1)
            time_str = self.scheduling_config.get('best_times', ['09:00'])[0]
            hour, minute = map(int, time_str.split(':'))
            return tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)

    def analyze_best_times(self):
        """
        Analyze and return best posting times based on TikTok engagement data

        Returns:
            dict: Analysis of best posting times
        """
        # General TikTok best practices
        analysis = {
            'weekday_best_times': [
                {'time': '09:00', 'reason': 'Morning commute, people checking phones'},
                {'time': '12:00', 'reason': 'Lunch break, high engagement'},
                {'time': '18:00', 'reason': 'After work/school, peak usage'},
                {'time': '21:00', 'reason': 'Evening relaxation, very high engagement'}
            ],
            'weekend_best_times': [
                {'time': '11:00', 'reason': 'Late morning, casual browsing'},
                {'time': '14:00', 'reason': 'Afternoon, leisure time'},
                {'time': '19:00', 'reason': 'Evening, peak weekend engagement'}
            ],
            'avoid_times': [
                {'time': '03:00-06:00', 'reason': 'Very low engagement, most users sleeping'},
                {'time': '23:00-02:00', 'reason': 'Lower engagement, winding down'}
            ],
            'tips': [
                'Post consistently at the same times',
                'Test different times and track performance',
                'Consider your target audience\'s schedule',
                'Weekends have different patterns than weekdays',
                'Holidays and events affect engagement'
            ]
        }

        return analysis

    def save_schedule(self, schedule, filename=None):
        """Save schedule to file"""
        if not filename:
            filename = f"schedule_{get_timestamp()}.json"

        filepath = f"output/{filename}"
        save_json(schedule, filepath)

        # Also create a readable version
        txt_filepath = filepath.replace('.json', '.txt')
        with open(txt_filepath, 'w', encoding='utf-8') as f:
            f.write("📅 TikTok POSTING SCHEDULE\n")
            f.write("=" * 60 + "\n\n")

            for item in schedule:
                f.write(f"Video #{item['video_number']}\n")
                f.write(f"  📆 Date: {item['date']} ({item['day_of_week']})\n")
                f.write(f"  🕐 Time: {item['time']} ({item['timezone']})\n")
                f.write(f"  🔗 Full: {item['datetime']}\n\n")

        return filepath


def main():
    """CLI for scheduler"""
    print("\n📅 TikTok Content Scheduler\n")

    scheduler = ContentScheduler()

    # Show best times analysis
    print("⏰ Best Posting Times Analysis:")
    print("=" * 60)

    analysis = scheduler.analyze_best_times()

    print("\n📈 Weekday Best Times:")
    for time_info in analysis['weekday_best_times']:
        print(f"  {time_info['time']} - {time_info['reason']}")

    print("\n📈 Weekend Best Times:")
    for time_info in analysis['weekend_best_times']:
        print(f"  {time_info['time']} - {time_info['reason']}")

    print("\n❌ Times to Avoid:")
    for time_info in analysis['avoid_times']:
        print(f"  {time_info['time']} - {time_info['reason']}")

    # Create sample schedule
    print("\n\n📋 Sample 7-Day Schedule (10 videos):")
    print("=" * 60)

    schedule = scheduler.create_schedule(video_count=10, days=7)

    for item in schedule[:5]:  # Show first 5
        print(f"Video #{item['video_number']}: {item['date']} at {item['time']}")

    print(f"... and {len(schedule) - 5} more")

    # Save schedule
    filepath = scheduler.save_schedule(schedule)
    print(f"\n💾 Full schedule saved to: {filepath}")


if __name__ == "__main__":
    main()

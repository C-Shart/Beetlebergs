import csv
from datetime import datetime, timezone
import io
import shutil
from team_color import TeamColor

class StatsManager:
    BATTLE_STARTED = "BATTLE_STARTED"
    BEETLE_DEAD = "BEETLE_DEAD"
    BATTLE_FINISHED = "BATTLE_FINISHED"

    STAT_NAMES = {
        BATTLE_STARTED: "BattlesStarted",
        BEETLE_DEAD: "BeetleDeaths",
        BATTLE_FINISHED: "BattlesFinished"
    }

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(StatsManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.stats = {}
        self.buffer = None
        self.writer = None
        self.start_time = None
        self.battle_number = 0

    def get_total_stat_key(self, stat_key):
        return f"TOTAL.{stat_key}"

    def get_team_stat_key(self, stat_key, team_color):
        return f"{team_color.name}.{stat_key}"

    def get_stat_name(self, stat_key):
        if "." in stat_key:
            key_parts = stat_key.split(".")
            base_name = __class__.STAT_NAMES[key_parts[1]]
            if key_parts[1] == __class__.BATTLE_FINISHED:
                base_name = "Wins"
            return f"{key_parts[0]}.{base_name}"
        else:
            return __class__.STAT_NAMES[stat_key]

    def get_stat(self, stat_key, team_color=TeamColor.NEUTRAL):
        if team_color == TeamColor.NEUTRAL:
            return self.stats[self.get_total_stat_key(stat_key)]
        else:
            return self.stats[self.get_team_stat_key(stat_key, team_color)]

    def set_stat(self, stat_key, stat_value, team_color=TeamColor.NEUTRAL):
        if team_color == TeamColor.NEUTRAL:
            self.stats[self.get_total_stat_key(stat_key)] = stat_value
        else:
            self.stats[self.get_team_stat_key(stat_key, team_color)] = stat_value

    def record_stat(self, stat_key,
                    team_a=TeamColor.NEUTRAL, actor_id_a=None, value_a=1, team_b=None, actor_id_b=None, value_b=None):
        total_stats_key = self.get_total_stat_key(stat_key)
        if total_stats_key not in self.stats:
            self.stats[total_stats_key] = value_a
        else:
            self.stats[total_stats_key] += value_a

        if team_a != TeamColor.NEUTRAL:
            team_stats_key = self.get_team_stat_key(stat_key, team_a)
            if team_stats_key not in self.stats:
                self.stats[team_stats_key] = value_a
            else:
                self.stats[team_stats_key] += value_a

        if self.buffer:
            team_a_name = team_a.name if team_a else team_a
            team_b_name = team_b.name if team_b else team_b
            self.write_detailed_stats_row(stat_key, team_a_name, actor_id_a, value_a, team_b_name, actor_id_b, value_b)

    def clear(self):
        self.stats.clear()
        if self.buffer:
            self.buffer.close()

    def start_detailed_stats(self):
        self.clear()
        self.buffer = io.StringIO(newline='')
        self.writer = csv.writer(self.buffer)
        self.writer.writerow(
            ["BattleNumber", "Timestamp", "Event", "TeamA", "ActorA", "ValueA", "TeamB", "ActorB", "ValueB"])
        self.start_time = datetime.now(timezone.utc)
        self.battle_number = 0

    def write_detailed_stats_row(self, event_type,
                                team_a, actor_a=None, value_a=1,
                                team_b=None, actor_b=None, value_b=None):
        self.writer.writerow([
            self.battle_number, datetime.now(timezone.utc), event_type,
            team_a, actor_a, value_a,
            team_b, actor_b, value_b])

    def start_battle(self, team_a, team_b):
        self.battle_number += 1
        if self.buffer:
            for beetle in team_a.beetles:
                self.write_detailed_stats_row(
                    __class__.BATTLE_STARTED,
                    team_a.color.name, beetle.team_index, beetle.hit_points,
                    value_b=beetle.__class__.__name__)
            for beetle in team_b.beetles:
                self.write_detailed_stats_row(
                    __class__.BATTLE_STARTED,
                    team_b.color.name, beetle.team_index, beetle.hit_points,
                    value_b=beetle.__class__.__name__)

    def save_detailed_stats(self):
        path = f"BeetlebergsDetailedStats{self.start_time.strftime('%Y%m%d%H%M')}.csv"
        with open(path, 'w', newline='', encoding="utf-8") as csv_file:
            self.buffer.seek(0)
            shutil.copyfileobj(self.buffer, csv_file)

StatsManager()
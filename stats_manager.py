from team_color import TeamColor

class StatsManager:
    BEETLE_DEAD = "BeetleDeaths"

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(StatsManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.stats = {}

    def get_total_stat_key(self, stat_key):
        return f"TOTAL.{stat_key}"

    def get_team_stat_key(self, stat_key, team_color):
        return f"{team_color}.{stat_key}"

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

    def record_stat(self, stat_key, step=1, team_color=TeamColor.NEUTRAL):
        total_stats_key = self.get_total_stat_key(stat_key)
        if total_stats_key not in self.stats:
            self.stats[total_stats_key] = step
        else:
            self.stats[total_stats_key] += step

        if team_color != TeamColor.NEUTRAL:
            team_stats_key = self.get_team_stat_key(stat_key, team_color)
            if team_stats_key not in self.stats:
                self.stats[team_stats_key] = step
            else:
                self.stats[team_stats_key] += step

    def clear(self):
        self.stats.clear()

StatsManager()
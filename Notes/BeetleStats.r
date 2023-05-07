library(tidyverse)

beetle_stat_events_raw <-
    read_csv("BeetlebergsDetailedStats202305070138.csv")

event_levels <- c(
    "BATTLE_STARTED",
    "STATE_CHANGED",
    "SHOT_FIRED",
    "SHOT_HIT",
    "DAMAGE_DEALT",
    "BEETLE_DEAD",
    "BATTLE_FINISHED")

team_levels <- c("GREEN", "RED")

beetle_stat_events <- beetle_stat_events_raw %>%
    transmute(
        BattleNumber,
        Timestamp,
        Event = parse_factor(Event, event_levels),
        TeamA = parse_factor(TeamA, team_levels),
        ActorA,
        ValueA,
        TeamB = parse_factor(TeamB, team_levels),
        ActorB,
        ValueB)

beetle_stat_events %>%
    filter(Event == "STATE_CHANGED") %>%
    group_by(TeamA, ActorA) %>%
    transmute(
        StateName = ValueA,
        StateEntered = Timestamp,
        StateExited = lead(Timestamp),
        Duration = StateExited - StateEntered
        ) %>%
    drop_na(Duration) %>%
    group_by(TeamA, ActorA, StateName) %>%
    summarize(TotalTimeSpentInState = sum(Duration)) %>%
    group_by(TeamA, StateName) %>%
    summarize(TotalTimeSpentInState = sum(TotalTimeSpentInState))

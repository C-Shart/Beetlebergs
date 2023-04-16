---
title: 🅱eetle 🅱attle 🅱tate 🅱achine 🅱iagram
---
Tasks

+ TASK_PRIMARY_ATTACK
+ TASK_SECONDARY_ATTACKS
+ TASK_CHANGE_TARGET (TASK_ACQUIRE_TARGET separate?)
+ TASK_FACE_TARGET
+ TASK MOVE_TOWARDS_TARGET
+ TASK_MAINTAIN_RANGE_FROM_TARGET
+ TASK_MOVE_AWAY_FROM_TARGET
+ TASK_
+ TASK_FIND_NEAREST_LONE_ALLY
+ TASK_FIND_NEAREST_ELITE
+ TASK_FIND_NEAREST_QUEEN
+ TASK_FIND_NEAREST_BOON
+ TASK_FIND_SAFEST_PLACE
+ TASK_FIND_STRONGEST_PLACE
+ TASK_DODGE_PROJECTILE
+ TASK_SET_WAYPOINT
+ TASK_MOVE_TOWARDS_WAYPOINT
+ TASK_DEVOUR
+ TASK_HALT_MOVEMENT
+ TASK_

Schedules

+ SCHEDULE_PUSH
+ SCHEDULE_HOLD
+ SCHEDULE_RETREAT
+ SCHEDULE_REGROUP
+ SCHEDULE_ACQUIRE_BOON
+ SCHEDULE_ACQUIRE_TARGET
+ SCHEDULE_MANEUVER
+ SCHEDULE_SEEK_QUEEN
+ SCHEDULE_SEEK_ELITE
+ SCHEDULE_SEEK_ALLY
+ SCHEDULE_

Goals

+ Attack
+ Seek

States

+ Searching
+ Engaged

Conditions

+

Sensors

+

Diagram

===

```mermaid
stateDiagram-v2
[*] --> StartIdle
StartIdle : Waiting For Battle Start
StartIdle --> FindTarget

FindTarget : Looking for Target
state FindTarget {
    [*] --> TargetNearby
    TargetNearby : Target Nearby?
    TargetNearby --> [*] : Target Acquired
    TargetNearby --> MoveRandomly : No
    MoveRandomly : Move Randomly
    MoveRandomly --> TargetNearby
}
FindTarget --> KillTarget : Target Acquired
FindTarget --> Dead : Beetle dies

KillTarget : Try to kill Target
state KillTarget {
    [*] --> TargetDead
    TargetDead : Target Dead?
    TargetDead --> AtRange : No
    TargetDead --> [*] : New Target
    AtRange : At Engagement Distance?
    AtRange --> MoveToRange : No
    MoveToRange : Move in Range
    MoveToRange --> FireAway
    AtRange --> FireAway : Yes
    FireAway : Fire at Target
    FireAway --> TargetDead
}
KillTarget --> FindTarget : New Target
KillTarget --> Dead : Beetle dies

Dead : Dead
Dead --> [*]


# Provider Examples

This file presents a series of [Provider examples](/provider).

## Table of Contents

- [Reports](#reports)

## Reports

For 3 months of provider operation in a city (September 2019 through November 2019) for 3 geographies, 2 vehicle types, and 1 special group. Values of `-1` represent [redacted data](#data-redaction) counts.

**September 2019** `/reports/2019-09.csv`

```csv
provider_id,start_date,duration,special_group_type,geography_id,vehicle_type,trip_count,rider_count
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,all_riders,44428624-186b-4fc3-a7fb-124f487464a1,scooter,1302,983
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,low_income,44428624-186b-4fc3-a7fb-124f487464a1,scooter,201,104
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,all_riders,44428624-186b-4fc3-a7fb-124f487464a1,bicycle,530,200
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,low_income,44428624-186b-4fc3-a7fb-124f487464a1,bicycle,75,26
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,all_riders,03db06d0-3998-406a-92c7-25a83fc2784a,scooter,687,450
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,low_income,03db06d0-3998-406a-92c7-25a83fc2784a,scooter,98,45
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,all_riders,03db06d0-3998-406a-92c7-25a83fc2784a,bicycle,256,104
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,low_income,03db06d0-3998-406a-92c7-25a83fc2784a,bicycle,41,16
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,all_riders,8ad39dc3-005b-4348-9d61-c830c54c161b,scooter,201,140
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,low_income,8ad39dc3-005b-4348-9d61-c830c54c161b,scooter,35,21
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,all_riders,8ad39dc3-005b-4348-9d61-c830c54c161b,bicycle,103,39
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,low_income,8ad39dc3-005b-4348-9d61-c830c54c161b,bicycle,15,-1
```

**October 2019** `/reports/2019-10.csv`

```csv
provider_id,start_date,duration,special_group_type,geography_id,vehicle_type,trip_count,rider_count
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,all_riders,44428624-186b-4fc3-a7fb-124f487464a1,scooter,1042,786
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,low_income,44428624-186b-4fc3-a7fb-124f487464a1,scooter,161,83
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,all_riders,44428624-186b-4fc3-a7fb-124f487464a1,bicycle,424,160
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,low_income,44428624-186b-4fc3-a7fb-124f487464a1,bicycle,60,0
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,all_riders,03db06d0-3998-406a-92c7-25a83fc2784a,scooter,550,360
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,low_income,03db06d0-3998-406a-92c7-25a83fc2784a,scooter,78,36
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,all_riders,03db06d0-3998-406a-92c7-25a83fc2784a,bicycle,205,83
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,low_income,03db06d0-3998-406a-92c7-25a83fc2784a,bicycle,33,13
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,all_riders,8ad39dc3-005b-4348-9d61-c830c54c161b,scooter,161,112
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,low_income,8ad39dc3-005b-4348-9d61-c830c54c161b,scooter,28,-1
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,all_riders,8ad39dc3-005b-4348-9d61-c830c54c161b,bicycle,82,31
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,low_income,8ad39dc3-005b-4348-9d61-c830c54c161b,bicycle,-1,0
```

**November 2019** `/reports/2019-11.csv`

```csv
provider_id,start_date,duration,special_group_type,geography_id,vehicle_type,trip_count,rider_count
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,all_riders,44428624-186b-4fc3-a7fb-124f487464a1,scooter,834,629
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,low_income,44428624-186b-4fc3-a7fb-124f487464a1,scooter,129,66
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,all_riders,44428624-186b-4fc3-a7fb-124f487464a1,bicycle,339,128
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,low_income,44428624-186b-4fc3-a7fb-124f487464a1,bicycle,48,-1
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,all_riders,03db06d0-3998-406a-92c7-25a83fc2784a,scooter,440,288
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,low_income,03db06d0-3998-406a-92c7-25a83fc2784a,scooter,62,29
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,all_riders,03db06d0-3998-406a-92c7-25a83fc2784a,bicycle,164,66
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,low_income,03db06d0-3998-406a-92c7-25a83fc2784a,bicycle,26,0
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,all_riders,8ad39dc3-005b-4348-9d61-c830c54c161b,scooter,129,90
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,low_income,8ad39dc3-005b-4348-9d61-c830c54c161b,scooter,22,-1
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,all_riders,8ad39dc3-005b-4348-9d61-c830c54c161b,bicycle,-1,25
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,low_income,8ad39dc3-005b-4348-9d61-c830c54c161b,bicycle,0,0
```

[Top][toc]

[toc]: #table-of-contents
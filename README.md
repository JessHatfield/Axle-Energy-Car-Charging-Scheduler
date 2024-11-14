# Axle Energy Coding Challenge - Car Charging Scheduler Backend


## My Solution

I've written a backend using Django Rest Framework then provided acceptance tests here demonstrating each of the behaviours in the acceptance criteria pdf.

I've been working DRF for the past couple of years at Qogita, so it seemed like a decent choice of tool for this exercise!

Its worth nothing that didn't have access to the latest version of the exercise (containing a pre-built streamlight application ) whilst I was writing this.

So building a REST API seemed like a reasonable course of action at the time.

Endpoint tests demonstrating each required behavior in the acceptance criteria can be found [here](https://github.com/JessHatfield/Axle-Energy-Car-Charging-Scheduler/blob/70cb7a5853c93a6479905829dae77fbb4f0dd791/CarChargingScheduler/tests/test_endpoints.py)


I made a couple of assumptions when it came to modelling:

- A user could have multiple cars but would only want to set a single charging schedule per car
- Charging schedules can spread across multiple days and need to be composed by discrete time ranges which cannot overlap
- The creation of Charging schedules/Charging Slots/Cars/Users would be something we would implement later
- The end user would always need to see the charging_schedule even if the schedule was currently paused or a car was not at home
- We need to support users across multiple different timezones

This is an example app made for the purposes of a code review. I've not tried to get it production ready:

- No authentication or env variable management was implemented
- We are not using a database which allows for simultaneous access
- I've not created a scalable project structure to allow for expansion across domains cleanly
- We have no logging or error tracking setup

I focused primarily on: 

- Coming up with domain model + set of relationships that meshed with our requirements and made sense to me
- Writing behavioural tests first and then writing our implementation to pass these tests
- Keeping the majority of our business logic separate from Model/View/Controller code via the services pattern
- Ensuring that we've supported a wide range of edge cases via regression testing, and that these extra cases did not pollute our endpoint test file 


## How to run

### Starting docker and running our tests

```shell
sudo sudo docker build -t car_charging_scheduler:latest .
sudo docker run -p 8000:8000 --name car_charging_scheduler -t car_charging_scheduler:latest
docker exec car_charging_scheduler pytest /app/CarChargingScheduler/tests
```

### Example API requests

#### Gets Cars For A User
```shell
curl -i -L  http://0.0.0.0:8000/car
```
Returns this payload. The `ae_id` field is used in requests to access other relevant endpoints.

```json
[
  {
    "is_at_home": true,
    "battery_level": "0.50",
    "ae_id": "9bdbad41-107d-4a4f-b43b-76b2852a4fa5"
  },
  {
    "is_at_home": true,
    "battery_level": "0.50",
    "ae_id": "757dc17c-cdf6-429a-8875-ac96b45fcd1b"
  }
]
```
#### Gets Charging Schedule For A Car

```shell
curl -i -L  http://0.0.0.0:8000/car/9bdbad41-107d-4a4f-b43b-76b2852a4fa5/charging_schedule/
```
Surfaces Our Charging Schedule including a projection of battery capacity once schedule is complete.

```json
{
  "paused_until": "2024-11-14T17:46:00.982257Z",
  "projected_battery_soc": 0.700,
  "charging_slots": [
    {
      "start_datetime": "2024-11-14T16:56:58.502550Z",
      "end_datetime": "2024-11-14T17:56:58.502551Z",
      "battery_level_gained": "0.10"
    },
    {
      "start_datetime": "2024-11-14T17:56:58.502948Z",
      "end_datetime": "2024-11-14T18:56:58.502951Z",
      "battery_level_gained": "0.10"
    },
    {
      "start_datetime": "2024-11-15T16:56:58.503322Z",
      "end_datetime": "2024-11-15T17:56:58.503324Z",
      "battery_level_gained": "0.10"
    }
  ],
  "is_schedule_paused": false,
  "is_override_applied": false
}
```
#### Trigger charging immediately

```shell
curl -X POST -i -L http://0.0.0.0:8000/car/9bdbad41-107d-4a4f-b43b-76b2852a4fa5/charging_schedule/override
```
Applies a 1hr override to our schedule which increases our projected_battery_soc by 0.1.

If the override partially overlaps with an existing slot, we apply a fraction of the override.

This behaviour is demonstrated within our test suite [here](https://github.com/JessHatfield/Axle-Energy-Car-Charging-Scheduler/blob/0221b64553f3a314b90d467db25b77df152bf7df/CarChargingScheduler/tests/services/test_battery_projection_calculator.py#L23).

#### Pause Charging Schedule

```shell
curl -X POST -i -L http://0.0.0.0:8000/car/9bdbad41-107d-4a4f-b43b-76b2852a4fa5/charging_schedule/pause
```

Pauses the charging schedule, preventing the added battery capacity from our charging slots from being applied to our projected_battery_soc.

The schedule will start to be applied again the following day.

This behaviour is demonstrated within our test suite [here](https://github.com/JessHatfield/Axle-Energy-Car-Charging-Scheduler/blob/67dd90e397a06ef9c307f65821e29f1ead623bad/CarChargingScheduler/tests/test_endpoints.py#L93-L136).

#### Mark Car As At-Home And Then Unmark Car As At-Home

```shell
curl -X PUT \
  -H "Content-Type: application/json" \
  -d '{"is_at_home": true}' \
  http://0.0.0.0:8000/car/9bdbad41-107d-4a4f-b43b-76b2852a4f
  
  curl -X PUT \
  -H "Content-Type: application/json" \
  -d '{"is_at_home": false}' \
  http://0.0.0.0:8000/car/9bdbad41-107d-4a4f-b43b-76b2852a4f
```

If a car is marked as being away from the home then the charging schedule is suspended. Battery capacity from our charging slots will not be applied to our projected_battery_soc.

This behaviour is demonstrated within our test suite [here](https://github.com/JessHatfield/Axle-Energy-Car-Charging-Scheduler/blob/67dd90e397a06ef9c307f65821e29f1ead623bad/CarChargingScheduler/tests/test_endpoints.py#L140).

In addition, overrides cannot be set whilst the car is not at home.

This behaviour is demonstrated within our test suite [here](https://github.com/JessHatfield/Axle-Energy-Car-Charging-Scheduler/blob/70cb7a5853c93a6479905829dae77fbb4f0dd791/CarChargingScheduler/tests/test_endpoints.py#L171-L185).




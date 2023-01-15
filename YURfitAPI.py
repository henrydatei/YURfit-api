import dataclasses
import requests
from datetime import datetime, timedelta
import dateutil.parser
from typing import List

import classes.User as User
import classes.Badge as Badge
import classes.Goal as Goal
import classes.LevelingProgress as LevelingProgress
import classes.GettingStarted as GettingStarted
import classes.WorkoutSources as WorkoutSources
import classes.Integration as Integration
import classes.Challenge as Challenge
import classes.Period as Period
import classes.Winner as Winner
import classes.Datapoint as Datapoint
import classes.FeedItem as FeedItem
import classes.Workout as Workout
import classes.Tag as Tag

@dataclasses.dataclass
class YURfitAPI:
    key: str

    # after login() avavilable
    token: str = dataclasses.field(init = False, default = None)
    email: str = dataclasses.field(init = False, default = None)
    displayName: str = dataclasses.field(init = False, default = None)
    localId: str = dataclasses.field(init = False, default = None)
    registered: bool = dataclasses.field(init = False, default = None)
    profilePicture: str = dataclasses.field(init = False, default = None)
    refreshToken: str = dataclasses.field(init = False, default = None)
    expiresAt: datetime = dataclasses.field(init = False, default = None)

    # after getAccountInfo() available
    passwordHash: str = dataclasses.field(init = False, default = None)
    emailVerified: bool = dataclasses.field(init = False, default = None)
    passwordUpdatedAt: datetime = dataclasses.field(init = False, default = None)
    validSince: datetime = dataclasses.field(init = False, default = None)
    lastLoginAt: datetime = dataclasses.field(init = False, default = None)
    createdAt: datetime = dataclasses.field(init = False, default = None)
    customAuth: bool = dataclasses.field(init = False, default = None)
    lastRefreshAt: datetime = dataclasses.field(init = False, default = None)

    def login(self, email, password) -> None:
        params = {"email": email, "password": password, "returnSecureToken": "true"}
        r = requests.post('https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={}'.format(self.key), data = params)
        r.raise_for_status()
        self.token = r.json()['idToken']
        self.email = r.json()['email']
        self.displayName = r.json()['displayName']
        self.localId = r.json()['localId']
        self.registered = r.json()['registered']
        self.profilePicture = r.json()['profilePicture']
        self.refreshToken = r.json()['refreshToken']
        self.expiresAt = datetime.now() + timedelta(seconds = int(r.json()['expiresIn']))

    def getAccountInfo(self) -> None:
        params = {"idToken": self.token}
        r = requests.post('https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={}'.format(self.key), data = params)
        r.raise_for_status()
        self.passwordHash = r.json()['users'][0]['passwordHash']
        self.emailVerified = r.json()['users'][0]['emailVerified']
        self.passwordUpdatedAt = datetime.fromtimestamp(int(r.json()['users'][0]['passwordUpdatedAt']) / 1000)
        self.validSince = datetime.fromtimestamp(int(r.json()['users'][0]['validSince']))
        self.lastLoginAt = datetime.fromtimestamp(int(r.json()['users'][0]['lastLoginAt']) / 1000)
        self.createdAt = datetime.fromtimestamp(int(r.json()['users'][0]['createdAt']) / 1000)
        self.customAuth = r.json()['users'][0]['customAuth']
        self.lastRefreshAt = dateutil.parser.parse(r.json()['users'][0]['lastRefreshAt'])

    def getUser(self) -> User.User:
        headers = {"Authorization": "Bearer " + self.token}
        r = requests.post('https://yurapp-502de.firebaseapp.com//api/v2/secure/user/biometrics/retrieve', headers = headers)
        r.raise_for_status()
        levelingProcess = LevelingProgress.LevelingProgress(**r.json()['levelingProgress'])
        dailyGoals = [Goal.Goal(**item) for item in r.json()['dailyGoal']]
        badges = [Badge.Badge(
            badgeTypeId = item['badgeTypeId'],
            badgeName = item['badgeName'],
            badgeDescription = item['badgeDescription'],
            badgeIconUrl = item['badgeIconUrl'],
            badgeImageUrl = item['badgeImageUrl'],
            badgeEarnedAt = datetime.fromtimestamp(int(item['badgeEarnedAt']) / 1000),
            startTime = datetime.fromtimestamp(int(item['startTime']) / 1000),
            endTime = datetime.fromtimestamp(int(item['endTime']) / 1000)
        ) for item in r.json()['badges']]
        return User.User(
            username = r.json()['username'],
            name = r.json()['name'],
            age = r.json()['age'],
            birthdate = datetime(year = r.json()['birthdate'][0], month = r.json()['birthdate'][1], day = r.json()['birthdate'][2]),
            customaryHeight = r.json()['customary']["height"],
            customaryWeight = r.json()['customary']["weight"],
            metricHeight = r.json()['metric']["height"],
            metricWeight = r.json()['metric']["weight"],
            metric_units = r.json()['metric_units'],
            sex = r.json()['sex'],
            photoURL = r.json()['photoURL'],
            timezone = r.json()['timezone'],
            totalXP = r.json()['totalXP'],
            rank = r.json()['rank'],
            levelingProcess = levelingProcess,
            uid = r.json()['uid'],
            userChallenges = [id for id in r.json()['userChallenges']],
            last_modified = datetime.fromtimestamp(r.json()['last_modified'] / 1000),
            dailyGoal = dailyGoals,
            overrideDailyGoal = r.json()['overrideDailyGoal'],
            automatchEnabled = r.json()['automatchEnabled'],
            badges = badges,
            isValid = r.json()['IsValid'],
            bioAdjust = r.json()['bioAdjust'],
            createdAt = datetime.fromtimestamp(r.json()['created_at'] / 1000)
        )

    def gettingStarted(self) -> GettingStarted.GettingStarted:
        headers = {"Authorization": "Bearer " + self.token}
        r = requests.get('https://yurapp-502de.firebaseapp.com/api/v3/user/{}/profile/gettingstarted'.format(self.localId), headers = headers)
        r.raise_for_status()
        return GettingStarted.GettingStarted(**r.json())

    def getWorkoutSources(self) -> WorkoutSources.WorkoutSources:
        headers = {"Authorization": "Bearer " + self.token}
        r = requests.get('https://yurapp-502de.firebaseapp.com/api/v3/user/{}/workoutsources'.format(self.localId), headers = headers)
        r.raise_for_status()
        return WorkoutSources.WorkoutSources(**r.json())

    def getOtherIntegrations(self) -> Integration.Integration:
        headers = {"Authorization": "Bearer " + self.token}
        r = requests.get('https://yurapp-502de.firebaseapp.com/api/v3/user/{}/otherintegrations'.format(self.localId), headers = headers)
        r.raise_for_status()
        return [Integration.Integration(**item) for item in r.json()]

    def getChallenges(self) -> List[Challenge.Challenge]:
        headers = {"Authorization": "Bearer " + self.token}
        r = requests.get('https://yurapp-502de.firebaseapp.com/api/v3/user/me/challenges', headers = headers)
        r.raise_for_status()
        challenges = []
        for challenge in r.json():
            periods = []
            for period in challenge['periods']:
                if "calories" in period["flagData"]:
                    calories = period["flagData"]['calories']
                else:
                    calories = 0
                if "steps" in period["flagData"]:
                    steps = period["flagData"]['steps']
                else:
                    steps = 0
                periods.append(Period.Period(
                    index = period['index'],
                    start = datetime.fromtimestamp(int(period['start'])),
                    end = datetime.fromtimestamp(int(period['end'])),
                    flags = period['flags'],
                    calories = calories,
                    steps = steps,
                    gameIds = period["flagData"]['game_ids']
                ))
            winners = []
            for winner in challenge['winners']:
                if "progress" in winner:
                    progress = [Datapoint.Datapoint(**item) for item in winner['progress']]
                else:
                    progress = []
                if "currentPeriod" in winner:
                    currentPeriod = Datapoint.Datapoint(**winner['currentPeriod'])
                else:
                    currentPeriod = None
                if "last_modified" in winner:
                    lastModified = datetime.fromtimestamp(int(winner['last_modified']) / 1000)
                else:
                    lastModified = None
                if "needs_update" in winner:
                    needsUpdate = winner['needs_update']
                else:
                    needsUpdate = None
                if "lastWorkoutTimestamp" in winner:
                    lastWorkout = datetime.fromtimestamp(int(winner['lastWorkoutTimestamp']))
                else:
                    lastWorkout = None
                winners.append(Winner.Winner(
                    active = winner['active'],
                    lastModified = lastModified,
                    progress = progress,
                    currentPeriod = currentPeriod,
                    photoUrl = winner['photo_url'],
                    needsUpdate = needsUpdate,
                    uid = winner['uid'],
                    lastWorkout = lastWorkout,
                    name = winner['name'],
                    currentProgress = Datapoint.Datapoint(**winner['currentProgress']),
                ))
            challenges.append(Challenge.Challenge(
                challengeId = challenge['challengeId'],
                name = challenge['name'],
                ownerUid = challenge['ownerUid'],
                permissionVisibility = challenge['permissions']["visibility"],
                permissionInvite = challenge['permissions']["invite"],
                isStarted = challenge['is_started'],
                isEnded = challenge['is_ended'],
                start = datetime.fromtimestamp(int(challenge['start'])),
                end = datetime.fromtimestamp(int(challenge['end'])),
                createdAt = datetime.fromtimestamp(int(challenge['created_at']) / 1000),
                timezone = challenge['timezone'],
                minChallengers = challenge['minChallengers'],
                maxChallengers = challenge['maxChallengers'],
                challengerCount = challenge['challengerCount'],
                periods = periods,
                lastModified = datetime.fromtimestamp(int(challenge['last_modified']) / 1000),
                startedAt = datetime.fromtimestamp(int(challenge['started_at']) / 1000),
                awaitChallenger = challenge['awaitChallenger'],
                winners = winners,
                imageUrl = challenge['image_url']
            ))
        return challenges

    def getGoals(self):
        headers = {"Authorization": "Bearer " + self.token}
        r = requests.get('https://yurapp-502de.firebaseapp.com/api/v3/user/goals', headers = headers)
        r.raise_for_status()
        return r.json()

    def getFeed(self, limit: int = 5, to_time: datetime = datetime.now()) -> List[FeedItem.FeedItem]:
        headers = {"Authorization": "Bearer " + self.token}
        params = {"limit": limit, "to_time": to_time.timestamp() * 1000}
        r = requests.get('https://yurapp-502de.firebaseapp.com/api/v3/user/wnWVKjAC8ISm6YSFvU714MndSV62/feed', headers = headers, params = params)
        r.raise_for_status()
        return [FeedItem.FeedItem(
            lastModified = datetime.fromtimestamp(item['last_modified'] / 1000),
            title = item['title'],
            ownerUid = item['ownerUid'],
            createdAt = datetime.fromtimestamp(item['created_at'] / 1000),
            date = datetime.fromtimestamp(item['date'] / 1000),
            hideMainFeed = item['hideMainFeed'],
            pictureUrl = item['picture_url'],
            type = item['type'],
            activityId = item['activityId'],
            meta = item['meta'],
        ) for item in r.json()["data"]]

    def getWorkouts(self, limit: int = 100000, from_time: datetime = datetime.now() - timedelta(days = 7), to_time: datetime = datetime.now()) -> List[Workout.Workout]:
        headers = {"Authorization": "Bearer " + self.token}
        r = requests.get('https://yurapp-502de.firebaseapp.com/api/v2/secure/workout/get', headers = headers)
        r.raise_for_status()
        workouts = []
        for workout in r.json()["documents"]:
            tags = [Tag.Tag(
                tag = tag['tag'],
                duration = tag['duration'],
                time = datetime.fromtimestamp(int(tag['timestamp']) / 1000),
                samplesIncluded = tag['samplesIncluded'],
                hmdDistanceTravelled = tag["metadata"]['hmdDistanceTravelled'],
                avgHeartRate = tag["metadata"]['avgHeartRate'],
                avgEstHeartRate = tag["metadata"]['avgEstHeartRate'],
                squats = tag["metadata"]['squats'],
                calories = tag["metadata"]['calories'],
                avgBurnRate = tag["metadata"]['avgBurnRate'],
                leftDistanceTravelled = tag["metadata"]['leftDistanceTravelled'],
                rightDistanceTravelled = tag["metadata"]['rightDistanceTravelled']
            ) for tag in workout['tags']]
            workouts.append(Workout.Workout(
                startTime = datetime.fromtimestamp(int(workout['startTime']) / 1000),
                endTime = datetime.fromtimestamp(int(workout['endTime']) / 1000),
                calories = workout['calories'],
                gameId = workout['gameID'],
                identifier = workout['identifier'],
                duration = workout['duration'],
                squats = workout['squats'],
                steps = workout['steps'],
                xp = workout['xp'],
                clientVersion = workout['clientVersion'],
                validity = workout['validity'],
                isOfflineWorkout = workout['isOfflineWorkout'],
                isWorkoutActive = workout['isWorkoutActive'],
                workoutId = workout['workoutID'],
                lastModified = datetime.fromtimestamp(int(workout['last_modified']) / 1000),
                sourceName = workout['sourceName'],
                tags = tags
            ))
        return workouts
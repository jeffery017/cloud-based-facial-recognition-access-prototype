
# Parameters

import random
from typing import List
from test import Guest, Cache0, Cache1, Cache2



class Params:
    def __init__(self, total_users, cache_size, ratio_daily, ratio_weekly, ratio_monthly):
        self.total_users = total_users  # Define total number of users in the system
        self.cache_size = cache_size  # Maximum number of unique users that can be cached at a time
        self.daily_avtive_user = int(total_users * ratio_daily)
        self.weekly_avtive_user = int(total_users * ratio_weekly)
        self.monthly_activt_user = int(total_users * ratio_monthly)
        
        # Costs
        self.wifi_bandwidth_per_request = 500  # in KB
        self.cache_hit_time_cost = 550  # in ms
        self.cache_miss_time_cost = 750  # in ms
        self.cache_miss_bandwidth_cost = 1  # in KB

        # Metrics
        self.total_bandwidth = 0
        self.total_wait_time = 0
        self.total_requests = 0
        self.len_mon = 3
        self.len_day = self.len_mon * 30
        self.len_hours = self.len_day * 24




def createGuests(params):
# create guest list
    guests = []
    i = 0
    # guests = [Guest(guest_id=0, frequency=2),Guest(guest_id=0, frequency=3)]
    for _ in range(params.daily_avtive_user):
        guests.append(Guest(guest_id=i, frequency=24))
        i += 1

    for _ in range(params.weekly_avtive_user):
        guests.append(Guest(guest_id=i, frequency=24 * 7))
        i += 1

    for _ in range(params.monthly_activt_user):
        guests.append(Guest(guest_id=i, frequency=24 * 30))
        i += 1

    random.shuffle(guests)
    return guests

def runCacheTest(guests, cache):
    # Simulate cache with set for caching active users
    for hour in range(params.len_hours):
        for guest in guests:
            if guest.nextVisit == hour:
                isHit = cache.guestVisit(guest) 
                guest.updatState(isHit)

    
def printTestResult(cache):
    print(f'\tcache: (hit: {cache.hitCount} / miss: {cache.missCount} / hit rate: {cache.hitCount/(cache.hitCount + cache.missCount)*100:.2f}%)')


def printTierGuestAverageWaitTime(guests: List[Guest]):
    totalTime = 0
    totalVisit = 0
    dailyGuest = []
    weeklyGuest = []
    monthlyGuest = []
    for guest in guests:
        if guest.frequency < 24 * 2:
            dailyGuest.append(guest.totalWaitTime/guest.visitCount)
        elif guest.frequency < 24 * 10:
            weeklyGuest.append(guest.totalWaitTime/guest.visitCount)
        else:
            monthlyGuest.append(guest.totalWaitTime/guest.visitCount)
        totalTime += guest.totalWaitTime
        totalVisit += guest.visitCount
    
    print(f"""\tAvg\tDaily\tWeekly\tMonthly)
\t{totalTime/totalVisit:.0f}\t{sum(dailyGuest)/len(dailyGuest):.0f}\t{sum(weeklyGuest)/len(weeklyGuest):.0f}\t{sum(monthlyGuest)/len(monthlyGuest):.0f}
""")
    
def printTrafficNeed(guests, params):
    totalTraffic = 0
    for guest in guests:
        totalTraffic += guest.totalTraffic
    print(f"\ttotal traffic: {(totalTraffic / params.len_mon/1000000):.0f} MB")


if __name__ == "__main__":
    # test 1
    guestCount = 5000
    gcRate = 0.1
    print(f"Guest/Cache ratio: {gcRate}")
    params = Params(guestCount, guestCount * gcRate, 0.1, 0.4, 0.5)
    caches = [Cache0(params.cache_size), Cache1(params.cache_size), Cache2(params.cache_size)]
    for i in range(3):
        guests = createGuests(params)
        runCacheTest(guests, caches[i])
        printTestResult(caches[i])
        printTrafficNeed(guests, params)
        #guest wait
        printTierGuestAverageWaitTime(guests)


    # test 2
    guestCount = 5000
    gcRate = 0.2
    print(f"Guest/Cache ratio: {gcRate}")
    params = Params(guestCount, guestCount * gcRate, 0.1, 0.4, 0.5)
    caches = [Cache0(params.cache_size), Cache1(params.cache_size), Cache2(params.cache_size)]
    for i in range(3):
        guests = createGuests(params)
        runCacheTest(guests, caches[i])
        printTestResult(caches[i])
        printTrafficNeed(guests, params)
        #guest wait
        printTierGuestAverageWaitTime(guests)  

    # test 3
    guestCount = 5000
    gcRate = 0.3
    print(f"Guest/Cache ratio: {gcRate}")
    params = Params(guestCount, guestCount * gcRate, 0.1, 0.4, 0.5)
    caches = [Cache0(params.cache_size), Cache1(params.cache_size), Cache2(params.cache_size)]
    for i in range(3):
        guests = createGuests(params)
        runCacheTest(guests, caches[i])
        printTestResult(caches[i])
        printTrafficNeed(guests, params)
        #guest wait
        printTierGuestAverageWaitTime(guests)  

    # test 4
    guestCount = 5000
    gcRate = 0.4
    print(f"Guest/Cache ratio: {gcRate}")
    params = Params(guestCount, guestCount * gcRate, 0.1, 0.4, 0.5)
    caches = [Cache0(params.cache_size), Cache1(params.cache_size), Cache2(params.cache_size)]
    for i in range(3):
        guests = createGuests(params)
        runCacheTest(guests, caches[i])
        printTestResult(caches[i])
        printTrafficNeed(guests, params)
        #guest wait
        printTierGuestAverageWaitTime(guests)
    
    # test 5
    guestCount = 5000
    gcRate = 0.5
    print(f"Guest/Cache ratio: {gcRate}")
    params = Params(guestCount, guestCount * gcRate, 0.1, 0.4, 0.5)
    caches = [Cache0(params.cache_size), Cache1(params.cache_size), Cache2(params.cache_size)]
    for i in range(3):
        guests = createGuests(params)
        runCacheTest(guests, caches[i])
        printTestResult(caches[i])
        printTrafficNeed(guests, params)
        #guest wait
        printTierGuestAverageWaitTime(guests)

from collections import deque
import numpy as np
import random
from abc import ABC, abstractmethod

hitTime = 500
hitTraffic = 0
missTime = 750 * 1.5
missTraffic = 1000


        
class Guest:
    def __init__(self, guest_id, frequency):
        self.guest_id = guest_id
        self.frequency = int( frequency * (0.5 + random.random()) )
        self.lastVisit = 0
        self.nextVisit = frequency
        self.visitCount = 0
        self.totalWaitTime = 0 
        self.totalTraffic = 0

    def updatState(self, isHit:bool):
        self.visitCount += 1
        self.lastVisit = self.nextVisit
        self.nextVisit += self.frequency
        if isHit:
            self.totalWaitTime += hitTime
            self.totalTraffic += hitTraffic
        else:
            self.totalWaitTime += missTime
            self.totalTraffic += missTraffic





# First In, First out
class Cache0: 
    def __init__(self, size):
        self.cache = []
        self.maxSize = size
        self.hitCount = 0
        self.missCount = 0

    def guestVisit(self, guest:Guest):
        if self.popGuest(guest):
            self.hitCount += 1
            result = True
        else:
            self.missCount += 1
            result = False
            self.insertGuest(guest)
        return result

    
    def popGuest(self, guest:Guest)-> bool:
        for i in range(len(self.cache)):
            if guest.guest_id == self.cache[i]:
                return True
        return False

    def insertGuest(self, guest: Guest):
        self.cache.append(guest.guest_id)
        if len(self.cache) == self.maxSize:
            self.cache.pop(0)



# Last in, last out
class Cache1: 
    def __init__(self, size):
        self.cache = []
        self.maxSize = size
        self.hitCount = 0
        self.missCount = 0

    def guestVisit(self, guest:Guest):
        if self.popGuest(guest):
            self.hitCount += 1
            result = True
        else:
            self.missCount += 1
            result = False
        self.insertGuest(guest)
        return result

    
    def popGuest(self, guest:Guest)-> bool:
        for i in range(len(self.cache)):
            if guest.guest_id == self.cache[i]:
                self.cache.pop(i)
                return True
        return False

    def insertGuest(self, guest: Guest):
        self.cache.append(guest.guest_id)
        if len(self.cache) == self.maxSize:
            self.cache.pop(0)

    
# 3 Tier priority
class Cache2: 
    def __init__(self, size):
        self.maxSize = [int(size*0.3), int(size*0.3), int(size*0.4)]
        self.caches = [Cache1(self.maxSize[0]),
                       Cache1(self.maxSize[1]),
                       Cache1(self.maxSize[2])
                        ]
        self.hitCount = 0
        self.missCount = 0
    

    def guestVisit(self, guest:Guest)-> bool:
        if self.popGuest(guest): 
            self.hitCount += 1
            result = True
        else:
            self.missCount += 1
            result = False
        
        self.insertGuest(guest)
        return result

        
    def popGuest(self, guest:Guest)-> bool:
        for cache in self.caches:
            if cache.popGuest(guest):
                return True
        return False
    
    def insertGuest(self, guest:Guest):
        guestFreq = guest.nextVisit - guest.lastVisit
        
        if guestFreq < 48:
            guestTier = 0
        elif guestFreq < 24 * 10:
            guestTier = 1
        else:
            guestTier = 2
        
        self.caches[guestTier].insertGuest(guest=guest)

        
        
        
        

                







    



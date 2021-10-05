"""
This file creates simulated values for a bandit common bandit problem about what ads to show on a certain page. Read more about the bandit problem here:
https://www.youtube.com/watch?v=e3L4VocZnnQ

There are 5 different ads to show. It does not matter if ads are organic or sponsored. The key point is that it's about showing a certain type of content, and based on
the user's context, one might be more relevant than another. In this example, I will add some meta information that are more relevant to tell to tell than story instead of being
technical relevant.

Available Ads:

AD 1 - organic ad about electric vehicles
AD 2 - organic ad about stocks
AD 3 - organic ad about sports  (will be removed after 5m)
AD 4 - sponsored ad about buying a new mobile phone
AD 5 - sponsored ad about a hiring position (will be added after 6m)

The algorithm will measure relevancy by its click through rate (ctr). This is a very common method to messure the so called reward, because as higher the ctr is
as higher the context is for the user. In praxis though, it might get more complex. A click on a certain ad might be different in regards of user happyness or revenue.

The context of a user is defined by:

- day of week (MO-SU)
- mobile device (IOS/Android)
- last category visited (cars, clothes, jobs)
- ads created (number >= 0)

To make it easy, a user can all the time only see 1 ad on the homepage. The question here is, what ad to show? When Ad 1 performs the best (ctr) for a user on Monday with an IOS,
who the last time visited the cars category, does the ad 1 is also the best performing one for a user with an Andriod device?

As more dimensions we get, as more interested segments will be created that by a lot of time by surprise, perform differently than we think.

To make it more practical, ads and context will change over time that should not be a problem for the algorithm.

The expected CTR For each context for each add will be randomized and printed when you run this file
"""

from random import random
from typing import List
from ad import Ad
from bandit_model import BanditModel
from context import Context
from math_utils import create_random_ctr, create_random_context_multipliers
from debug_utils import get_formatted_time, print_existing_context_values_for_each_add_for_each_context, print_best_ad_for_each_context_with_ctr
from plot_utils import plot_array_data
import time


ADS = [
    Ad(id=1, ctr=create_random_ctr(), name="organic electric vehicles"),
    Ad(id=2, ctr=create_random_ctr(), name="organic stocks"),
    Ad(id=3, ctr=create_random_ctr(), name="organic sports"),
    Ad(id=4, ctr=create_random_ctr(), name="sponsored new mobile phone"),
]

DELAYED_AD = [
    Ad(id=5, ctr=create_random_ctr(), name="sponsored hiring position"),
]

CONTEXTS = {
    "DAY_OF_WEEK": [
        Context(name="MO", ctr_multiplier=create_random_context_multipliers(ADS)), 
        Context(name="TU", ctr_multiplier=create_random_context_multipliers(ADS)),
        Context(name="WED", ctr_multiplier=create_random_context_multipliers(ADS)),
        Context(name="THUR", ctr_multiplier=create_random_context_multipliers(ADS)), 
        Context(name="FRI", ctr_multiplier=create_random_context_multipliers(ADS)),
        Context(name="SAT", ctr_multiplier=create_random_context_multipliers(ADS)),
        Context(name="SUN", ctr_multiplier=create_random_context_multipliers(ADS)),
    ],

    "MOBILE_DEVICE": [
        Context(name="IOS", ctr_multiplier=create_random_context_multipliers(ADS)),
        Context(name="ANDROID", ctr_multiplier=create_random_context_multipliers(ADS)),
    ],

    "LAST_CATEGORY_VISITED": [
        Context(name="CARS", ctr_multiplier=create_random_context_multipliers(ADS)),
        Context(name="CLOTHS", ctr_multiplier=create_random_context_multipliers(ADS)),
        Context(name="JOBS", ctr_multiplier=create_random_context_multipliers(ADS)),
    ]
}

CONTEXTS_DELAYED = {
    "ADS_CREATED": [
        Context(name="0", ctr_multiplier=create_random_context_multipliers(ADS+DELAYED_AD)), 
        Context(name="1", ctr_multiplier=create_random_context_multipliers(ADS+DELAYED_AD)), 
        Context(name="2", ctr_multiplier=create_random_context_multipliers(ADS+DELAYED_AD)), 
        Context(name="3", ctr_multiplier=create_random_context_multipliers(ADS+DELAYED_AD)),
        Context(name="4", ctr_multiplier=create_random_context_multipliers(ADS+DELAYED_AD)), 
        Context(name="5", ctr_multiplier=create_random_context_multipliers(ADS+DELAYED_AD)), 
        Context(name="6", ctr_multiplier=create_random_context_multipliers(ADS+DELAYED_AD)), 
        Context(name="7", ctr_multiplier=create_random_context_multipliers(ADS+DELAYED_AD)), 
        Context(name="8", ctr_multiplier=create_random_context_multipliers(ADS+DELAYED_AD)), 
        Context(name="9", ctr_multiplier=create_random_context_multipliers(ADS+DELAYED_AD))
    ]
}

start_time = time.time()
current_time = time.time()

def main():
    global current_time, ADS, CONTEXTS

    # This print's the expected outcome
    # The algorithm does not know anything about CTRs, but they are different by ad and by context
    # The algorithm needs to explore it by itself, and exploit once recognized the best ad for the given context
    # 
    # In practice, it's a lot harder. These ctr's might change just over time, because certain
    # dimensions are not know. Also, ads and contexts change over time.
    
    print_existing_context_values_for_each_add_for_each_context(ADS, CONTEXTS, with_delayed_context=False)
    print_best_ad_for_each_context_with_ctr(ADS, CONTEXTS, with_delayed_context=False)

    rewards = []
    predictions_for_single_context = []
    bandit_model = BanditModel(ADS, CONTEXTS)

    simulation_runtime_in_seconds = start_time + 60*10

    loop_i = 0
    while current_time < simulation_runtime_in_seconds:
        print(f"Current time is: {get_formatted_time(current_time)}")
        print(f"Last 5 rewards: {rewards[-5:]}")
        print(f"Last 5 predictions for MO,IOS,CARS context: {predictions_for_single_context[-5:]}")

        # Contextual bandites are fun to write ourself, but for now, we will just use a library that simply works and explore a bit existing settings and mabye
        # constraints.
        #
        # In the books and docs, it looks simple and is advertised ad battle proofed, but in reality your problem might have special requirements that are not covered. If this is 
        # the case, you end up having a hard time to customize the library to your needs.

        # ask the model what to choose for a given context
        for context_value_day_of_week in CONTEXTS["DAY_OF_WEEK"]:
            for context_value_mobile_device in CONTEXTS["MOBILE_DEVICE"]:
                for context_value_last_category_visited in CONTEXTS["LAST_CATEGORY_VISITED"]:
                                            
                    current_context = [context_value_day_of_week.name, context_value_mobile_device.name, context_value_last_category_visited.name]
                    action_ad_index, prob = bandit_model.predict(current_context)

                    action_ad = ADS[action_ad_index]
                    current_ctr = action_ad.ctr * context_value_day_of_week.ctr_multiplier[action_ad] * context_value_mobile_device.ctr_multiplier[action_ad] * context_value_last_category_visited.ctr_multiplier[action_ad]

                    # train the model
                    random_number = random()
                    click_happened = random_number < current_ctr 
                    #click_happened = action_ad_index == 1 # force it

                    # print(f"LEARN Current context [{current_context}], action index [{action_ad_index}], click happened [{click_happened}]")
                    bandit_model.learn(current_context, action_ad_index, click_happened, prob)

                    if context_value_day_of_week.name == "MO" and context_value_mobile_device.name == "IOS" and context_value_last_category_visited.name == "CARS":
                        predictions_for_single_context.append(action_ad.name)
                        rewards.append(current_ctr)

                    
                    
        
        #time.sleep(1)
        current_time = time.time()

        if loop_i % 1000 == 0:
            plot_array_data(rewards, "rewards")

        loop_i += 1


            

if __name__ == "__main__":
    main()
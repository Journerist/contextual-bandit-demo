import random
import numpy as np
from sklearn.linear_model import LogisticRegression
from copy import deepcopy
from vowpalwabbit import pyvw

class BanditModel:

    def __init__(self, ads, contexts) -> None:
        self.vw = self.__create_bandit_model(ads)
        self.ads = ads
        np.random.seed(1)

        # for all context combinations and targets, we will create some seed data to enable the internal model to explore all contexts and all ads
        for context_value_day_of_week in contexts["DAY_OF_WEEK"]:
            for context_value_mobile_device in contexts["MOBILE_DEVICE"]:
                for context_value_last_category_visited in contexts["LAST_CATEGORY_VISITED"]:
                    action = np.random.randint(0, len(ads))
                    self.learn([context_value_day_of_week.name, context_value_mobile_device.name, context_value_last_category_visited.name], action, 0, 1/len(ads))
            
    def predict(self, current_context_arr):
        predict_str = self.__to_vw_example_format(current_context_arr, list(range(1,len(self.ads)+1)))
        # predict_str = self.__create_context_str(current_context_arr)

        print(f"predict: {predict_str}")


        choice = self.vw.predict(predict_str)

        chosen_action_index, prob = self.__sample_custom_pmf(choice)

        #print(f"chosen_action_index: {chosen_action_index}, prob: {prob}")

        return chosen_action_index, prob
    
    def learn(self, current_context_arr, ad_index, click_happened, prob):
        click_happened_int = int(click_happened == True)
        cost = click_happened_int * -1

        #learn_str = str(ad_index+1) + ":" + str(cost) + ":" + str(1/len(self.ads)) + " " +  self.__create_context_str(current_context_arr)
        learn_str = self.__to_vw_example_format(current_context_arr, list(range(1,len(self.ads)+1)), (ad_index+1, cost, prob))

        self.__learn(learn_str)  
    
    def __sample_custom_pmf(self, pmf):
        total = sum(pmf)
        scale = 1 / total
        pmf = [x * scale for x in pmf]
        draw = random.random()
        sum_prob = 0.0
        for index, prob in enumerate(pmf):
            sum_prob += prob
            if(sum_prob > draw):
                return index, prob

    def __learn(self, learn_str):
        print(f"learn: {learn_str}")
        self.vw.learn(learn_str)

    def __create_context_str(self, current_context_arr):
        predict_str = "|"

        for context_element in current_context_arr:
            predict_str += " " + context_element
        return predict_str


    def __create_bandit_model(self, ads):
        vw = pyvw.vw(f"--cb_explore_adf -q UA --quiet --first 2000")
        #vw = pyvw.vw(f"--cb_explore {str(len(ads))} --quiet --first 2000")

        return vw
    
    def __to_vw_example_format(self, context, actions, cb_label = None):
        if cb_label is not None:
            chosen_action, cost, prob = cb_label
        example_string = ""
        example_string += "shared |User day={} device={} category={}\n".format(context[0], context[1], context[2])
        for action in actions:
            if cb_label is not None and action == chosen_action:
                example_string += "0:{}:{} ".format(cost, prob)
            example_string += "|Target target={} \n".format(action)
        #Strip the last newline
        return example_string[:-1]

import time
from typing import List

from ad import Ad
from context import Context

def get_formatted_time(seconds_since_epoch):
    timeObj = time.localtime(seconds_since_epoch)

    return '%02d/%02d/%04d %02d:%02d:%02d' % (
    timeObj.tm_mday, timeObj.tm_mon, timeObj.tm_year, timeObj.tm_hour, timeObj.tm_min, timeObj.tm_sec)


def print_existing_context_values_for_each_add_for_each_context(ads: List[Ad], contexts: dict[str, list[Context]], with_delayed_context):

    print("### CTR FOR ALL ADS:")
    for ad in ads:
        print(f"*{ad.name}[", end="")
        for context_value_day_of_week in contexts["DAY_OF_WEEK"]:
            for context_value_mobile_device in contexts["MOBILE_DEVICE"]:
                for context_value_last_category_visited in contexts["LAST_CATEGORY_VISITED"]:
                    
                    if with_delayed_context is False:
                        print(f"DAY_OF_WEEK={context_value_day_of_week.name}, MOBILE_DEVICE={context_value_mobile_device.name}, LAST_CATEGORY_VISITED={context_value_last_category_visited.name}]", end="")
                        print(context_value_day_of_week)
                        
                        ad_ctr_for_context = ad.ctr * context_value_day_of_week.ctr_multiplier[ad] * context_value_mobile_device.ctr_multiplier[ad] * context_value_last_category_visited.ctr_multiplier[ad]
                        print(f"={ad_ctr_for_context}")
                    
                    else:

                        for context_value_ads_created in contexts["ADS_CREATED"]:
                            print(f"DAY_OF_WEEK={context_value_day_of_week.name}, MOBILE_DEVICE={context_value_mobile_device.name}, LAST_CATEGORY_VISITED={context_value_last_category_visited.name}, ADS_CREATED={context_value_ads_created.name}]", end="")
                            ad_ctr_for_context = ad.ctr * context_value_day_of_week.ctr_multiplier[ad] * context_value_mobile_device.ctr_multiplier[ad] * context_value_last_category_visited.ctr_multiplier[ad] * context_value_ads_created.ctr_multiplier[ad]
                            print(f"={ad_ctr_for_context}")


        print("")


def print_best_ad_for_each_context_with_ctr(ads: List[Ad], contexts: dict[str, list[Context]], with_delayed_context):

    print("### BEST ADS FOR EACH CONTEXT WITH CTR:")

    best_ad_per_context_with_ctr = {}

    for ad in ads:
        for context_value_day_of_week in contexts["DAY_OF_WEEK"]:
            for context_value_mobile_device in contexts["MOBILE_DEVICE"]:
                for context_value_last_category_visited in contexts["LAST_CATEGORY_VISITED"]:
                    
                    if with_delayed_context is False:
                        context_str = f"[DAY_OF_WEEK={context_value_day_of_week.name}, MOBILE_DEVICE={context_value_mobile_device.name}, LAST_CATEGORY_VISITED={context_value_last_category_visited.name}]"
                        ad_ctr_for_context = ad.ctr * context_value_day_of_week.ctr_multiplier[ad] * context_value_mobile_device.ctr_multiplier[ad] * context_value_last_category_visited.ctr_multiplier[ad]
                       
                        update_best_ad_per_context_if_ctr_better(best_ad_per_context_with_ctr, ad, context_str, ad_ctr_for_context)
                    else:

                        for context_value_ads_created in contexts["ADS_CREATED"]:
                            context_str = f"[DAY_OF_WEEK={context_value_day_of_week.name}, MOBILE_DEVICE={context_value_mobile_device.name}, LAST_CATEGORY_VISITED={context_value_last_category_visited.name}, ADS_CREATED={context_value_ads_created.name}]"
                            ad_ctr_for_context = ad.ctr * context_value_day_of_week.ctr_multiplier[ad] * context_value_mobile_device.ctr_multiplier[ad] * context_value_last_category_visited.ctr_multiplier[ad] * context_value_ads_created.ctr_multiplier[ad]
                            
                            update_best_ad_per_context_if_ctr_better(best_ad_per_context_with_ctr, ad, context_str, ad_ctr_for_context)

    for context_str, performance_data in best_ad_per_context_with_ctr.items():
        print(f"for Context {context_str} the ad {performance_data['ad_name']} perfoms the best with ctr {performance_data['ctr']}")


def update_best_ad_per_context_if_ctr_better(best_ad_per_context_with_ctr, ad, context_str, ad_ctr_for_context):
    if context_str not in best_ad_per_context_with_ctr.keys():
        best_ad_per_context_with_ctr[context_str] = {
            "ad_name": ad.name,
            "ctr": ad_ctr_for_context
        }

    if (best_ad_per_context_with_ctr[context_str]["ctr"] < ad_ctr_for_context):
            best_ad_per_context_with_ctr[context_str]["ctr"] = ad_ctr_for_context
            best_ad_per_context_with_ctr[context_str]["ad_name"] = ad.name
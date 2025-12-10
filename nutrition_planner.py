# to pick from a array of foods randomly
import random

# pandas to store and alter food data
import pandas as pd

# activity level multiplyer per pound, based on how high or low activty is
factors = {
        "low": 12.0,
        "medium": 14.0,
        "high": 16.0,
        }


class Person:
    """
    Class storing users personal weight goals

    Attributes
    ----------
    current_w : float
        Current weight input by user, in pounds
    goal_w : float
        Goal weight input by user, in pounds
    timeline : float
        User input in weeks for when they want to be at goal weight 
    activity : str ('low', 'medium', 'high')
        User selection for how active they are each week
    health_concern : Boolean
        Health concerns that will create concern for saturated fat (True or False)
    """

    def __init__(self, current_w, goal_w, timeline,
                 activity, health_concern= False,
                 calorie_target = 2000, sat_fat = 1):
        
        self.current_w = current_w
        self.goal_w = goal_w
        self.timeline = timeline
        self.activity = activity
        self.health_concern = health_concern
        self.calorie_target = calorie_target
        self.fiber_grams = (self.calorie_target / 1000) * 14
        self.sat_fat = ((calorie_target * 0.07) / 9)


    def goal_type(self):
        """
        Determine if the users wants to gain, lose, or maintain their weight

        Return : str
            'lose', 'gain', or 'maintain' based on goal weight.
        """
        if self.goal_w < self.current_w:
            return "lose"
        elif self.goal_w > self.current_w:
            return "gain"
        return "maintain"
    

    def daily_calorie_target(self):
        """
        Calculate estimated daily calories needed to reach goal weight
        within the user's chosen timeline, and validifies if timeline is possible.

        Returns
        -------
        calorie_target : float
            Estimated daily calorie intake for weight goal.
        unhealthy : boolean
            determines if the weight lose goal is unhealthy if its more than 1000 cals/day
        """

        maintenance = maintain_cals(self.current_w, self.activity)

        # compute difference, could be negative or positive
        pounds_change = self.goal_w - self.current_w

        # 1 pound is 3500, multiple pounds needed for change by calories to convert 
        total_calorie_shift = pounds_change * 3500
    
        # Spread across timeline, and convert weeks to days, use 1 if timeline is unusable
        days = max(self.timeline * 7, 1)

        daily_adjustment = total_calorie_shift / days

        # if user loses or gains more than 1000 calories per day = unhealthy
        unhealthy = abs(daily_adjustment) > 1000

        calorie_target = maintenance + daily_adjustment

        return calorie_target, unhealthy


    def protein_grams(self):
        """
        Estimate grams of protein needed per day based on user weight
        and goal type (lose, gain, or maintain).

        Returns
        -------
        self.current_w * multiplier : float
           Recommended grams of protein per day.
        """
        goal = self.goal_type()

        # higher protein when trying to lose weight
        if goal == "lose":
           multiplier = 1.0
        else:
            multiplier = 0.8

        return self.current_w * multiplier
    


def maintain_cals(weight_lb, activity_level):
    """
    Estimate daily maintenance calories based on weight and activity.

    Parameters
    ----------
    weight_lb : float
        Body weight in pounds.
    activity_level : str
        One of 'low', 'medium', or 'high'.

    Returns
    -------
    maintain : float
        Estimated number of calories needed per day to maintain weight.
    """

    # pulls activity level in lowercase, defaulting to 14 if input improperly
    factor = factors.get(activity_level.lower(), 14.0)

    maintain = weight_lb * factor 

    return maintain
        

class FoodDatabase:
    """
    Store example low- and high-calorie food options and methods 
    to view and generate meals.

    Attributes
    ----------
    low_cal : dict
        food categories with lists of (name, calories)
        for lower calorie foods
    high_cal : dict
        food categories with lists of (name, calories)
        for higher calorie foods
    """

    def __init__(self):
        # low calorie foods, name with amount, calories
        self.low_cal = {
            "protein": [
                ("chicken breast, 100g", 165),
                ("tofu, 100g", 80),
                ("egg whites, 3 large", 50),
            ],
            "dairy": [
                ("nonfat Greek yogurt, 150g", 90),
                ("skim milk, 1 cup", 80),
            ],
            "veggies": [
                ("spinach, 2 cups", 20),
                ("broccoli, 1 cup", 55),
            ],
            "grain": [
                ("brown rice, 1/2 cup cooked", 110),
                ("quinoa, 185g", 222),
            ],
        }

        self.high_cal = {
            "protein": [("peanut butter, 32g", 188),
                        ("ground beef, 100g", 250)
                        ],

            "dairy": [("cheddar cheese, 1 oz", 115),
                      ("whole milk, 1 cup", 150)
                      ],

            "veggies": [("sweet potato, 1 medium", 110),
                        ("avocado, 1/2", 120)
                        ],

            "grain": [("white rice, 1 cup cooked", 200),
                      ("pasta, 1 cup cooked", 220)
                      ],
        }

    def store_food_df(self, group="low"):
        """
        Convert stored foods to a pandas DataFrame.

        Parameters
        ----------
        group : str
            low for low-calorie foods, high for high-calorie foods

        Returns
        -------
        df.sort_values("calories") : pandas.DataFrame
            table of foods with group, category, name, and calories
        """
        if group == "low":
            source = self.low_cal
            label = "low_cal"
        else:
            source = self.high_cal
            label = "high_cal"

        rows = []
        for category, foods in source.items():
            for name, cals in foods:
                rows.append({
                    "group": label,
                    "category": category,
                    "food": name,
                    "calories": cals,
                })

        df = pd.DataFrame(rows)
        return df.sort_values("calories")


    def random_meal(self, person):
        """
        Generate a meal based to someone's goal (lose vs gain), give them ingredients from 
        each catergory of meal type

        Parameters
        ----------
        person : Person
            The user instance to evaluate goal type.

        Returns
        -------
        meal_items : list of str
            foods selected from each category for the meal
        total_cals : int
            sum of calories from selected foods
        group_used : str
            food group was selected, low or high
        """

        # Decide group automatically based on goal
        if person.goal_type() == "lose":
            source = self.low_cal
            group = "low"
        elif person.goal_type() == "gain":
            source = self.high_cal
            group = "high"
        else:
            # maintain does random pick of either low/high cal foods
            source = random.choice([self.low_cal, self.high_cal])
            group = "balanced"

        meal_items = []
        total_cals = 0

        for category, foods in source.items():
            name, cals = random.choice(foods)
            meal_items.append(f"{category}: {name}")
            total_cals += cals

        return meal_items, total_cals, group
    

    
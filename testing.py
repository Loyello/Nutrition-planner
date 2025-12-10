from nutrition_planner import Person, maintain_cals, FoodDatabase


def test_goal_type():
    # example people for each weight goal scenario, tests if weight goals align with output
    p_lose = Person(160, 140, 12, "medium")
    p_gain = Person(120, 150, 12, "medium")
    p_same = Person(150, 150, 12, "medium")

    # assert if lose, gain, and maintain are accurate to weight goals
    assert p_lose.goal_type() == "lose"
    assert p_gain.goal_type() == "gain"
    assert p_same.goal_type() == "maintain"


def test_maintain_cals():
    """
    Test that maintenance calories increase with higher activity levels 
    for the same body weight. The calculated calories match the chosen 
    multipliers. Activity level input is case-insensitive

    """
    # default example weight
    weight = 150

    low_cals = maintain_cals(weight, "low")
    med_cals = maintain_cals(weight, "medium")
    high_cals = maintain_cals(weight, "high")

    # Higher activity should have higher maintenance calories
    assert med_cals > low_cals
    assert high_cals > med_cals

    # Checks calculations, # 150 * 12 = 1800, 150 * 14 = 2100, 150 * 16 = 2400
    assert low_cals == 1800
    assert med_cals == 2100
    assert high_cals == 2400

    # Check case sensitivity of  input
    med_caps = maintain_cals(weight, "MEDIUM")
    med_rand = maintain_cals(weight, "MeDiUM")
    assert med_caps == med_cals
    assert med_rand == med_cals


def test_daily_calorie_target():
    """
    Test that daily_calorie_target increases calories for weight gain
    and decreases calories for weight loss, relative to maintenance.
    """
    # Same starting weight and activity
    p_gain = Person(150, 170, 10, "medium")
    p_lose = Person(150, 130, 10, "medium")

    maintenance = maintain_cals(150, "medium")

    gain_target, gain_unhealthy = p_gain.daily_calorie_target()
    lose_target, lose_unhealthy = p_lose.daily_calorie_target()

    assert gain_target > maintenance
    assert lose_target < maintenance
    assert gain_unhealthy is False
    assert lose_unhealthy is False

def test_protein_grams():
    """
    Test that protein_grams recommends more protein when goal is 
    weight lose
    """

    p_lose = Person(150, 130, 12, "medium")
    p_gain = Person(150, 170, 12, "medium")

    protein_lose = p_lose.protein_grams()
    protein_gain = p_gain.protein_grams()

    assert protein_lose > protein_gain


def test_random_meal():
    """
    test FoodDatabase.random_meal returns a meal_items is a non-empty list,
    entries are strings, total calories is numeric + positive, 
    group is one of expected labels

    """
    db = FoodDatabase()
    p = Person(150, 140, 8, "medium")

    meal_items, total_cals, group = db.random_meal(p)

    assert isinstance(meal_items, list)
    assert len(meal_items) > 0
    assert isinstance(total_cals, (int, float))
    assert total_cals > 0

    assert group in ("low", "high", "balanced")


    

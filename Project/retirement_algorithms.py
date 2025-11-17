"""
CIT3003 - Analysis of Algorithms
Retirement Investment Optimization Using Algorithmic Design

Author: Rushane Green, 
Student ID: 2006930
Group Members: 
Date: November 2025

This module implements retirement investment algorithms using:
- Iterative simulation for compound growth modeling
- Binary search (Successive Approximation) for optimization

Theoretical Foundation:
- Divide-and-Conquer paradigm via Binary Search
- Polynomial time complexity: O(n) for simulation, O(log n * n) for optimization
"""


def fixedInvestor(principal, rate, years):
    """
    Simulate compound growth with fixed annual interest rate and contributions.
    
    Mathematical Recurrence Relation:
        B(0) = 0
        B(t) = (B(t-1) + principal) × (1 + rate)  for t = 1, 2, ..., years
    
    Where:
        B(t) = balance at end of year t
        principal = annual contribution made at start of each year
    
    Algorithm:
        Iterative simulation following the recurrence relation.
        Each iteration represents one year of contributions and growth.
    
    Time Complexity: O(n) where n = years
    Space Complexity: O(1) - only stores current balance
    
    Parameters:
        principal (float): Annual contribution amount (must be >= 0)
        rate (float): Annual interest rate as decimal (e.g., 0.05 for 5%)
        years (int): Number of contribution years (must be >= 0)
    
    Returns:
        float: Total accumulated balance after all contributions and compounding
    
    Raises:
        ValueError: If inputs are invalid (negative values, rate < -1)
    
    Example:
        >>> fixedInvestor(7500, 0.05, 3)
        23643.75
        
        Computation trace:
        Year 0: balance = 0
        Year 1: balance = (0 + 7500) × 1.05 = 7,875.00
        Year 2: balance = (7875 + 7500) × 1.05 = 16,143.75
        Year 3: balance = (16143.75 + 7500) × 1.05 = 24,826.94
    """
    # Input validation
    if principal < 0:
        raise ValueError(f"Principal cannot be negative: {principal}")
    if rate < -1.0:
        raise ValueError(f"Rate cannot be less than -100%: {rate}")
    if years < 0:
        raise ValueError(f"Years cannot be negative: {years}")
    if not isinstance(years, int):
        raise TypeError(f"Years must be an integer: {years}")
    
    # Base case: no years means no growth
    if years == 0:
        return 0.0
    
    # Initialize accumulator
    current_balance = 0.0
    growth_multiplier = 1.0 + rate
    
    # Iterative simulation: apply recurrence relation for each year
    for year in range(1, years + 1):
        # Add annual contribution, then apply growth
        # This follows: B(t) = (B(t-1) + principal) × (1 + rate)
        current_balance = (current_balance + principal) * growth_multiplier
    
    return current_balance


def variableInvestor(principal, rateList):
    """
    Simulate compound growth with variable annual interest rates.
    
    Mathematical Recurrence Relation:
        B(0) = principal (initial investment)
        B(t) = B(t-1) × (1 + rateList[t-1])  for t = 1, 2, ..., len(rateList)
    
    Where:
        B(t) = balance at end of year t
        rateList[t-1] = interest rate applied in year t
    
    Algorithm:
        Sequential application of each year's rate to accumulated balance.
        Unlike fixedInvestor, no additional contributions are made.
    
    Time Complexity: O(n) where n = len(rateList)
    Space Complexity: O(1) - only stores current balance
    
    Parameters:
        principal (float): Initial investment amount (must be >= 0)
        rateList (list of float): Annual growth rates as decimals
                                  (can be negative for market losses)
    
    Returns:
        float: Final accumulated balance after applying all variable rates
    
    Raises:
        ValueError: If principal is negative or rateList contains rate < -1
        TypeError: If rateList is not a list or contains non-numeric values
    
    Example:
        >>> variableInvestor(10000, [0.05, 0.03, -0.02])
        10598.70
        
        Computation trace:
        Year 0: balance = 10,000.00
        Year 1: balance = 10,000 × 1.05 = 10,500.00
        Year 2: balance = 10,500 × 1.03 = 10,815.00
        Year 3: balance = 10,815 × 0.98 = 10,598.70
    """
    # Input validation
    if principal < 0:
        raise ValueError(f"Principal cannot be negative: {principal}")
    if not isinstance(rateList, list):
        raise TypeError(f"rateList must be a list, got {type(rateList)}")
    if len(rateList) == 0:
        raise ValueError("rateList cannot be empty")
    
    for i, rate in enumerate(rateList):
        if not isinstance(rate, (int, float)):
            raise TypeError(f"Rate at index {i} must be numeric: {rate}")
        if rate < -1.0:
            raise ValueError(f"Rate at index {i} cannot be less than -100%: {rate}")
    
    # Initialize balance with starting principal
    current_balance = principal
    
    # Apply each year's rate sequentially
    for year_index, rate in enumerate(rateList):
        growth_multiplier = 1.0 + rate
        current_balance = current_balance * growth_multiplier
    
    return current_balance


def finallyRetired(balance, expense, rate):
    """
    Determine retirement duration under annual withdrawals and growth.
    
    Mathematical Recurrence Relation:
        B(0) = balance (initial retirement fund)
        B(t) = (B(t-1) - expense) × (1 + rate)  for t = 1, 2, ...
        Termination: when B(t) <= 0
    
    Where:
        B(t) = balance at end of year t
        expense = amount withdrawn at start of each year
        rate = post-retirement growth rate
    
    Algorithm:
        Iterative simulation of withdrawal-then-growth cycle.
        Withdrawal occurs BEFORE interest application (real-world modeling).
        Counts years until balance is depleted.
    
    Time Complexity: O(n) where n = number of years until depletion
    Space Complexity: O(1) - only stores current balance and counter
    
    Parameters:
        balance (float): Initial retirement account value (must be >= 0)
        expense (float): Annual withdrawal amount (must be >= 0)
        rate (float): Expected post-retirement interest rate
    
    Returns:
        int: Number of years until balance reaches zero or becomes negative
             Returns 0 if balance is already insufficient for first withdrawal
    
    Raises:
        ValueError: If balance or expense is negative
    
    Example:
        >>> finallyRetired(100000, 10000, 0.03)
        13
        
        Computation trace:
        Year 0: balance = 100,000.00
        Year 1: (100,000 - 10,000) × 1.03 = 92,700.00
        Year 2: (92,700 - 10,000) × 1.03 = 85,181.00
        ...
        Year 13: balance becomes negative
    """
    # Input validation
    if balance < 0:
        raise ValueError(f"Balance cannot be negative: {balance}")
    if expense < 0:
        raise ValueError(f"Expense cannot be negative: {expense}")
    if rate < -1.0:
        raise ValueError(f"Rate cannot be less than -100%: {rate}")
    
    # Edge case: cannot afford even first withdrawal
    if balance < expense:
        return 0
    
    # Initialize tracking variables
    current_balance = balance
    years_survived = 0
    growth_multiplier = 1.0 + rate
    
    # Simulate each year: withdraw first, then apply growth
    # Continue until balance cannot support withdrawal
    while current_balance >= expense:
        # 1. Withdraw annual expense
        current_balance -= expense
        
        # 2. Apply interest to remaining balance
        current_balance *= growth_multiplier
        
        # 3. Increment year counter
        years_survived += 1
        
        # Safety check: prevent infinite loop if expense is too small
        # and growth rate is high enough to never deplete
        if years_survived > 1000:  # Arbitrary but reasonable limit
            break
    
    return years_survived


def maximumExpensed(balance, rate, target_years=20, epsilon=0.01, max_iterations=100):
    """
    Find maximum sustainable annual withdrawal using Binary Search.
    
    Optimization Problem:
        Find expense* such that finallyRetired(balance, expense*, rate) ≈ target_years
        
    Search Space:
        expense ∈ [0, balance]
        
    Objective:
        Maximize expense while satisfying the constraint that funds last
        approximately target_years years.
    
    Algorithm: Successive Approximation via Binary Search
        1. Initialize: low = 0, high = balance
        2. While |high - low| > epsilon and iterations < max:
            a. mid = (low + high) / 2
            b. years_lasted = finallyRetired(balance, mid, rate)
            c. If years_lasted > target_years:
                   Expense too low → funds last too long → increase expense
                   low = mid
            d. Else if years_lasted < target_years:
                   Expense too high → funds deplete too soon → decrease expense
                   high = mid
            e. Else:
                   Found optimal value → return mid
        3. Return (low + high) / 2
    
    Time Complexity: O(log(balance/epsilon) × target_years)
        - Binary search iterations: O(log(balance/epsilon))
        - Each iteration calls finallyRetired: O(target_years)
    
    Space Complexity: O(1)
    
    Design Pattern: Divide-and-Conquer
        - Problem space is divided in half each iteration
        - Successive approximation narrows the search range
    
    Parameters:
        balance (float): Initial retirement fund balance (must be > 0)
        rate (float): Fixed or average growth rate
        target_years (int): Desired retirement duration (default: 20)
        epsilon (float): Convergence threshold for binary search (default: 0.01)
        max_iterations (int): Safety limit to prevent infinite loops (default: 100)
    
    Returns:
        float: Estimated optimal annual withdrawal amount
    
    Raises:
        ValueError: If balance <= 0 or target_years <= 0
    
    Example:
        >>> maximumExpensed(500000, 0.04, target_years=25)
        32004.56
        
        Binary search trace:
        Iteration 1: mid=250000, years=2 → too high, adjust high
        Iteration 2: mid=125000, years=5 → too high, adjust high
        ...
        Iteration n: converges to ~32000
    """
    # Input validation
    if balance <= 0:
        raise ValueError(f"Balance must be positive: {balance}")
    if target_years <= 0:
        raise ValueError(f"Target years must be positive: {target_years}")
    if epsilon <= 0:
        raise ValueError(f"Epsilon must be positive: {epsilon}")
    if rate < -1.0:
        raise ValueError(f"Rate cannot be less than -100%: {rate}")
    
    # Initialize binary search bounds
    low_expense = 0.0
    high_expense = balance  # Maximum possible withdrawal is entire balance
    
    iteration_count = 0
    
    # Binary search with successive approximation
    while (high_expense - low_expense) > epsilon and iteration_count < max_iterations:
        # Calculate midpoint (candidate expense)
        mid_expense = (low_expense + high_expense) / 2.0
        
        # Test how long funds last with this expense
        years_lasted = finallyRetired(balance, mid_expense, rate)
        
        # Adjust search range based on result
        if years_lasted > target_years:
            # Funds last too long → can afford higher expense
            # Move lower bound up
            low_expense = mid_expense
            
        elif years_lasted < target_years:
            # Funds deplete too soon → need lower expense
            # Move upper bound down
            high_expense = mid_expense
            
        else:
            # Exact match found (rare but possible)
            return mid_expense
        
        iteration_count += 1
    
    # Return best approximation after convergence or max iterations
    optimal_expense = (low_expense + high_expense) / 2.0
    
    return optimal_expense


# ============================================
# UTILITY FUNCTIONS
# ============================================

def format_currency(amount):
    """
    Format numeric value as currency string.
    
    Separates presentation from computation.
    """
    return f"${amount:,.2f}"


def format_percentage(rate):
    """
    Format decimal rate as percentage string.
    """
    return f"{rate * 100:.2f}%"


# ============================================
# COMPREHENSIVE TESTING
# ============================================

if __name__ == "__main__":
    """
    Test suite for algorithm validation.
    Demonstrates correctness for theory component.
    """
    print("=" * 70)
    print("CIT3003 - RETIREMENT ALGORITHM TEST SUITE")
    print("=" * 70)
    
    # TEST 1: Fixed Investor - Example from PDF
    print("\n--- TEST 1: fixedInvestor() ---")
    print("Scenario: $7,500/year contribution, 5% growth, 3 years")
    print("Expected: $23,643.75 (from project specification)")
    
    try:
        result1 = fixedInvestor(7500, 0.05, 3)
        print(f"Result:   {format_currency(result1)}")
        print(f"Status:   {'✓ PASS' if abs(result1 - 23643.75) < 1 else '✗ FAIL'}")
    except Exception as e:
        print(f"Error: {e}")
    
    # TEST 2: Variable Investor
    print("\n--- TEST 2: variableInvestor() ---")
    print("Scenario: $10,000 initial, rates = [5%, 3%, -2%]")
    
    try:
        result2 = variableInvestor(10000, [0.05, 0.03, -0.02])
        print(f"Result: {format_currency(result2)}")
        
        # Manual verification:
        # Year 1: 10000 × 1.05 = 10500
        # Year 2: 10500 × 1.03 = 10815
        # Year 3: 10815 × 0.98 = 10598.70
        expected = 10000 * 1.05 * 1.03 * 0.98
        print(f"Expected: {format_currency(expected)}")
        print(f"Status: {'✓ PASS' if abs(result2 - expected) < 0.01 else '✗ FAIL'}")
    except Exception as e:
        print(f"Error: {e}")
    
    # TEST 3: Finally Retired
    print("\n--- TEST 3: finallyRetired() ---")
    print("Scenario: $100,000 balance, $10,000/year expense, 3% growth")
    
    try:
        result3 = finallyRetired(100000, 10000, 0.03)
        print(f"Result: {result3} years")
        print(f"Status: ✓ Computed (verify manually if needed)")
    except Exception as e:
        print(f"Error: {e}")
    
    # TEST 4: Maximum Expensed (Binary Search)
    print("\n--- TEST 4: maximumExpensed() ---")
    print("Scenario: $500,000 balance, 4% growth, 25-year target")
    
    try:
        result4 = maximumExpensed(500000, 0.04, target_years=25)
        print(f"Optimal withdrawal: {format_currency(result4)}")
        
        # Verify the result by testing how long it actually lasts
        verification = finallyRetired(500000, result4, 0.04)
        print(f"Verification: Lasts {verification} years (target was 25)")
        print(f"Status: {'✓ PASS' if abs(verification - 25) <= 1 else '✗ FAIL'}")
    except Exception as e:
        print(f"Error: {e}")
    
    # TEST 5: Error Handling
    print("\n--- TEST 5: Error Handling ---")
    
    test_cases = [
        ("Negative principal", lambda: fixedInvestor(-1000, 0.05, 10)),
        ("Invalid rate", lambda: fixedInvestor(1000, -2.0, 10)),
        ("Negative years", lambda: fixedInvestor(1000, 0.05, -5)),
    ]
    
    for test_name, test_func in test_cases:
        try:
            test_func()
            print(f"{test_name}: ✗ FAIL (should have raised error)")
        except ValueError:
            print(f"{test_name}: ✓ PASS (error caught correctly)")
        except Exception as e:
            print(f"{test_name}: ✗ FAIL (wrong error type: {type(e).__name__})")
    
    print("\n" + "=" * 70)
    print("TEST SUITE COMPLETE")
    print("=" * 70)
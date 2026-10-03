import os
import json

questions = []

def add_q(category, topic, difficulty, question, options, answer_index, explanation, hint_l1="", hint_l2=""):
    questions.append({
        "question": question,
        "options": options,
        "answer_index": answer_index,
        "topic": topic,
        "category": category,
        "difficulty": difficulty,
        "explanation": explanation,
        "hint_l1": hint_l1,
        "hint_l2": hint_l2
    })

# ==========================================
# 1. QUANTITATIVE APTITUDE (52 Questions: 20 Easy, 20 Medium, 12 Hard)
# ==========================================

# --- 20 Easy Quantitative ---
add_q("Quantitative", "Numbers", "easy",
      "What is the value of 15% of 480?",
      ["64", "72", "76", "80"], 1,
      "10% of 480 = 48. 5% of 480 = 24. 15% = 48 + 24 = 72.",
      "Break down 15% into 10% + 5% for quick mental calculation.",
      "Calculate 10% of 480 by moving the decimal, then halve that for 5%, and add them.")

add_q("Quantitative", "Numbers", "easy",
      "Find the sum of the first 20 natural numbers.",
      ["190", "200", "210", "220"], 2,
      "Sum of first n natural numbers = n(n + 1)/2 = 20 * 21 / 2 = 210.",
      "Use the standard arithmetic progression sum formula n(n+1)/2.",
      "Substitute n = 20: (20 * 21) / 2.")

add_q("Quantitative", "Numbers", "easy",
      "Which of the following numbers is prime?",
      ["51", "67", "87", "91"], 1,
      "51 = 3 * 17; 87 = 3 * 29; 91 = 7 * 13. 67 has no factors other than 1 and itself.",
      "Check divisibility by prime numbers up to sqrt(100) = 2, 3, 5, 7.",
      "Test 51 (5+1=6, div by 3), 87 (8+7=15, div by 3), 91 (7*13=91). 67 is not divisible by 2, 3, 5, or 7.")

add_q("Quantitative", "Percentages", "easy",
      "A student scored 340 marks out of 500 in an examination. What is the percentage of marks obtained?",
      ["64%", "68%", "72%", "75%"], 1,
      "Percentage = (340 / 500) * 100 = 68%.",
      "Divide the obtained marks by total marks and multiply by 100.",
      "340 / 500 = 34 / 50 = 68 / 100 = 68%.")

add_q("Quantitative", "Percentages", "easy",
      "If the price of an article increases from $80 to $100, what is the percentage increase?",
      ["20%", "25%", "30%", "35%"], 1,
      "Increase = 100 - 80 = 20. % Increase = (20 / 80) * 100 = 25%.",
      "Percentage increase = (Absolute Increase / Original Value) * 100.",
      "Change is 20 on an original base of 80: (20/80) = 1/4 = 25%.")

add_q("Quantitative", "Profit & Loss", "easy",
      "A shopkeeper purchases an item for $150 and sells it for $180. What is his profit percentage?",
      ["15%", "20%", "25%", "30%"], 1,
      "Profit = 180 - 150 = $30. Profit % = (30 / 150) * 100 = 20%.",
      "Profit % is always calculated with respect to Cost Price (CP).",
      "Profit = SP - CP = 30. Calculate (30 / 150) * 100.")

add_q("Quantitative", "Profit & Loss", "easy",
      "An article bought for $400 is sold at a loss of 15%. What is the selling price?",
      ["$320", "$340", "$350", "$360"], 1,
      "Loss = 15% of 400 = 0.15 * 400 = $60. Selling Price = 400 - 60 = $340.",
      "Selling Price = Cost Price * (1 - Loss%/100).",
      "Loss is 0.15 * 400 = 60. Subtract 60 from 400.")

add_q("Quantitative", "Ratio & Proportion", "easy",
      "If A : B = 2 : 3 and B : C = 4 : 5, what is the compound ratio A : B : C?",
      ["8 : 12 : 15", "6 : 9 : 10", "8 : 10 : 15", "2 : 4 : 5"], 0,
      "Multiply A:B by 4 -> 8:12. Multiply B:C by 3 -> 12:15. Hence A : B : C = 8 : 12 : 15.",
      "Equalize the common term B in both ratios by multiplying appropriate factors.",
      "Make B = 12 in both: (2*4):(3*4) and (4*3):(5*3) gives 8 : 12 : 15.")

add_q("Quantitative", "Ratio & Proportion", "easy",
      "Two numbers are in the ratio 4 : 7. If their sum is 132, what is the smaller number?",
      ["44", "48", "52", "56"], 1,
      "Total parts = 4 + 7 = 11 parts = 132. 1 part = 12. Smaller number = 4 * 12 = 48.",
      "Divide the total sum by the sum of ratio parts to find the value of one unit.",
      "132 / (4 + 7) = 132 / 11 = 12. Smaller number = 4 * 12.")

add_q("Quantitative", "Average", "easy",
      "Find the average of 24, 36, 48, 60, and 72.",
      ["44", "48", "50", "52"], 1,
      "The numbers form an arithmetic progression. In an odd-termed AP, the average is the middle term = 48.",
      "Notice that the numbers are evenly spaced by 12.",
      "Sum = 240. Average = 240 / 5 = 48 (or simply middle term in AP).")

add_q("Quantitative", "Average", "easy",
      "The average of 4 numbers is 25. If three of the numbers are 18, 22, and 28, find the fourth number?",
      ["28", "30", "32", "34"], 2,
      "Total sum = 4 * 25 = 100. Sum of three numbers = 18 + 22 + 28 = 68. Fourth number = 100 - 68 = 32.",
      "Total sum = Average * Count.",
      "Compute 4 * 25 = 100 and subtract 18 + 22 + 28 = 68.")

add_q("Quantitative", "Time & Work", "easy",
      "A can finish a task in 10 days and B in 15 days. In how many days can they complete it together?",
      ["5 days", "6 days", "7.5 days", "8 days"], 1,
      "Work done per day = 1/10 + 1/15 = 5/30 = 1/6. Days required = 6 days.",
      "Use the combined work formula: (A * B) / (A + B).",
      "(10 * 15) / (10 + 15) = 150 / 25 = 6 days.")

add_q("Quantitative", "Time & Work", "easy",
      "Pipe A fills an empty water tank in 8 hours. What fraction of the tank does it fill in 5 hours?",
      ["1/2", "5/8", "3/8", "5/6"], 1,
      "Rate per hour = 1/8. In 5 hours, fraction filled = 5 * (1/8) = 5/8.",
      "Multiply the hourly fill rate by the number of hours.",
      "Hourly rate is 1/8. Multiply by 5.")

add_q("Quantitative", "Time, Speed & Distance", "easy",
      "Convert a speed of 72 km/h into meters per second (m/s).",
      ["15 m/s", "20 m/s", "25 m/s", "30 m/s"], 1,
      "Multiply by 5/18: 72 * (5/18) = 4 * 5 = 20 m/s.",
      "The conversion factor from km/h to m/s is 5/18.",
      "72 * (5 / 18) = 4 * 5.")

add_q("Quantitative", "Time, Speed & Distance", "easy",
      "A bus travels a distance of 180 km in 3 hours. What is its speed?",
      ["50 km/h", "60 km/h", "70 km/h", "80 km/h"], 1,
      "Speed = Distance / Time = 180 / 3 = 60 km/h.",
      "Use Speed = Distance / Time.",
      "180 / 3 = 60 km/h.")

add_q("Quantitative", "Probability", "easy",
      "What is the probability of getting an even number when rolling a standard fair six-sided die?",
      ["1/6", "1/3", "1/2", "2/3"], 2,
      "Even numbers are {2, 4, 6} (3 outcomes out of 6). Probability = 3/6 = 1/2.",
      "Identify the favorable outcomes out of total sample space {1, 2, 3, 4, 5, 6}.",
      "Favorable = {2, 4, 6} = 3. Total = 6. 3/6 = 1/2.")

add_q("Quantitative", "Probability", "easy",
      "A coin is tossed twice. What is the probability of getting at least one Head?",
      ["1/4", "1/2", "3/4", "1"], 2,
      "Sample space: {HH, HT, TH, TT}. At least one head: {HH, HT, TH} = 3/4.",
      "At least one head is the complement of getting two tails (TT).",
      "Total outcomes = 4. Only TT has no heads. Probability = 1 - 1/4 = 3/4.")

add_q("Quantitative", "Algebra", "easy",
      "If 4x - 7 = 21, what is the value of x?",
      ["5", "6", "7", "8"], 2,
      "4x = 21 + 7 = 28 => x = 28 / 4 = 7.",
      "Isolate x by adding 7 to both sides, then divide by 4.",
      "4x = 28, so x = 7.")

add_q("Quantitative", "Mensuration", "easy",
      "What is the perimeter of a rectangle having length 14 cm and width 9 cm?",
      ["42 cm", "46 cm", "50 cm", "54 cm"], 1,
      "Perimeter = 2 * (length + width) = 2 * (14 + 9) = 2 * 23 = 46 cm.",
      "Perimeter formula for a rectangle is 2(l + w).",
      "2 * (14 + 9) = 2 * 23 = 46 cm.")

add_q("Quantitative", "Clocks", "easy",
      "How many degrees does the minute hand of a clock turn in 25 minutes?",
      ["120°", "140°", "150°", "160°"], 2,
      "The minute hand turns 360° in 60 minutes = 6° per minute. In 25 minutes: 25 * 6° = 150°.",
      "Minute hand moves 360° / 60 = 6° per minute.",
      "Multiply 25 by 6°.")

# --- 20 Medium Quantitative ---
add_q("Quantitative", "Percentages", "medium",
      "If Sales increased from $80,000 in 2024 to $104,000 in 2025, what was the percentage increase?",
      ["25%", "30%", "32%", "35%"], 1,
      "Increase = 104,000 - 80,000 = 24,000. % Increase = (24,000 / 80,000) * 100 = 30%.",
      "Find the net difference and divide by the baseline year value.",
      "24,000 / 80,000 = 3/10 = 30%.")

add_q("Quantitative", "Percentages", "medium",
      "In a competitive exam, 40% passed in Math and 60% passed in English. If 25% passed in both, what % failed in both?",
      ["20%", "25%", "30%", "35%"], 1,
      "Passed in at least one = 40% + 60% - 25% = 75%. Failed in both = 100% - 75% = 25%.",
      "Use set union formula: n(A U B) = n(A) + n(B) - n(A ∩ B).",
      "100 - (40 + 60 - 25) = 100 - 75 = 25%.")

add_q("Quantitative", "Profit & Loss", "medium",
      "A merchant marks an article 35% above cost and offers a discount of 20%. What is his net profit percentage?",
      ["6%", "8%", "10%", "12%"], 1,
      "Let CP = 100. MP = 135. SP = 135 * 0.80 = 108. Profit = 8%.",
      "Effective multiplier is 1.35 * 0.80.",
      "1.35 * 0.80 = 1.08, which represents an 8% gain over 1.00.")

add_q("Quantitative", "Ratio & Proportion", "medium",
      "Two numbers are in the ratio 3 : 5. If 9 is subtracted from each, the new ratio becomes 12 : 23. What is the smaller number?",
      ["27", "33", "36", "45"], 1,
      "(3x - 9)/(5x - 9) = 12/23 => 69x - 207 = 60x - 108 => 9x = 99 => x = 11. Smaller number = 3 * 11 = 33.",
      "Set up the algebraic fraction (3x - 9)/(5x - 9) = 12/23 and cross-multiply.",
      "69x - 207 = 60x - 108 leads to 9x = 99.")

add_q("Quantitative", "Average", "medium",
      "The average age of a class of 30 students is 15 years. If the teacher's age is included, the average increases by 1 year. What is the teacher's age?",
      ["42 years", "44 years", "46 years", "48 years"], 2,
      "Initial total = 30 * 15 = 450. New total for 31 people = 31 * 16 = 496. Teacher = 496 - 450 = 46 years.",
      "Teacher's age = Old Average + (New Count * Increase).",
      "15 + 31 * 1 = 46 years.")

add_q("Quantitative", "Time & Work", "medium",
      "Two pipes A and B can fill a tank in 12 minutes and 18 minutes respectively. If both are opened together, how long will it take?",
      ["6.2 minutes", "7.2 minutes", "8.0 minutes", "8.5 minutes"], 1,
      "Work per minute = 1/12 + 1/18 = 5/36. Time = 36/5 = 7.2 minutes.",
      "Product over sum: (12 * 18) / (12 + 18).",
      "216 / 30 = 7.2 minutes.")

add_q("Quantitative", "Time, Speed & Distance", "medium",
      "A train 240m long crosses a pole in 16 seconds and crosses a platform in 36 seconds. What is the length of the platform?",
      ["260m", "280m", "300m", "320m"], 2,
      "Speed = 240/16 = 15 m/s. Platform crossing: 240 + P = 15 * 36 = 540 => P = 300m.",
      "Calculate train speed from pole crossing first.",
      "Speed is 15 m/s. In 36s it covers 540m. Platform = 540 - 240.")

add_q("Quantitative", "Time, Speed & Distance", "medium",
      "A speed boat goes 30 km downstream and returns upstream in 4 hours 30 minutes. Current speed is 5 km/h. Find boat speed in still water.",
      ["12 km/h", "15 km/h", "18 km/h", "20 km/h"], 1,
      "30/(v+5) + 30/(v-5) = 4.5. Testing v = 15: 30/20 + 30/10 = 1.5 + 3 = 4.5 hrs. Boat speed = 15 km/h.",
      "Set up time equation: D/(v + c) + D/(v - c) = Total Time.",
      "Substitute options into 30/(v+5) + 30/(v-5) = 4.5.")

add_q("Quantitative", "Probability", "medium",
      "Two dice are thrown simultaneously. What is the probability that the sum of the numbers is a prime number?",
      ["5/12", "7/12", "1/2", "5/36"], 0,
      "Prime sums are 2, 3, 5, 7, 11. Outcomes: 1+2+4+6+2 = 15. Probability = 15/36 = 5/12.",
      "List the favorable pairs summing to 2, 3, 5, 7, and 11.",
      "Favorable pairs count is 15. Total is 36. 15/36 = 5/12.")

add_q("Quantitative", "Permutation & Combination", "medium",
      "In how many ways can the letters of the word 'LEADER' be arranged?",
      ["180", "360", "720", "1440"], 1,
      "Total letters = 6, with E repeated 2 times. Ways = 6! / 2! = 720 / 2 = 360.",
      "Use permutations of multiset: n! / (p! * q!).",
      "6! / 2! = 720 / 2 = 360.")

add_q("Quantitative", "Numbers", "medium",
      "What is the remainder when (17^200) is divided by 18?",
      ["1", "2", "17", "0"], 0,
      "17 ≡ -1 (mod 18). So 17^200 ≡ (-1)^200 = 1 (mod 18).",
      "Express 17 as (18 - 1) and apply binomial expansion.",
      "(-1)^200 = 1.")

add_q("Quantitative", "Mixture & Alligation", "medium",
      "In what ratio must tea at $62/kg be mixed with tea at $72/kg so that the mixture is worth $65/kg?",
      ["7 : 3", "3 : 7", "5 : 3", "3 : 5"], 0,
      "Rule of Alligation: (72 - 65) : (65 - 62) = 7 : 3.",
      "Alligation ratio = (Dearer Price - Mean) : (Mean - Cheaper Price).",
      "(72 - 65) : (65 - 62) = 7 : 3.")

add_q("Quantitative", "Calendar", "medium",
      "If 15th August 2011 was a Monday, what day of the week was 15th August 2012?",
      ["Tuesday", "Wednesday", "Thursday", "Friday"], 1,
      "2012 is a leap year with Feb 29 falling between the two dates. Days = 366 mod 7 = 2 odd days. Monday + 2 = Wednesday.",
      "Check if February 29th falls within the date interval.",
      "It spans Feb 2012 (29 days), so add 2 days to Monday.")

add_q("Quantitative", "Algebra", "medium",
      "If x + y = 12 and xy = 32, what is the value of x^2 + y^2?",
      ["72", "80", "88", "96"], 1,
      "x^2 + y^2 = (x + y)^2 - 2xy = 12^2 - 2(32) = 144 - 64 = 80.",
      "Use algebraic identity: (x + y)^2 = x^2 + y^2 + 2xy.",
      "144 - 2(32) = 80.")

add_q("Quantitative", "Mensuration", "medium",
      "The perimeter of a square is equal to the perimeter of a rectangle of dimensions 16 cm by 12 cm. Find the area of the square.",
      ["169 cm^2", "196 cm^2", "225 cm^2", "256 cm^2"], 1,
      "Perimeter = 2(16 + 12) = 56 cm. Side of square = 56 / 4 = 14 cm. Area = 14^2 = 196 cm^2.",
      "Find rectangle perimeter first, then divide by 4 to get square side.",
      "2 * 28 = 56. Side = 14. Area = 14 * 14 = 196.")

add_q("Quantitative", "Progression", "medium",
      "Find the 10th term of the arithmetic progression: 7, 11, 15, 19, ...",
      ["39", "43", "47", "51"], 1,
      "a = 7, d = 4. T_10 = a + (10 - 1)d = 7 + 9(4) = 7 + 36 = 43.",
      "Formula for n-th term of an AP is T_n = a + (n - 1)d.",
      "7 + 9 * 4 = 43.")

add_q("Quantitative", "Percentages", "medium",
      "A number is first increased by 20% and then decreased by 20%. What is the net percentage change?",
      ["No change", "2% decrease", "4% decrease", "4% increase"], 2,
      "Net change = +20 - 20 - (20*20)/100 = -4% (4% decrease).",
      "Successive percentage formula: a + b + (ab/100).",
      "20 - 20 - 400/100 = -4%.")

add_q("Quantitative", "Time & Work", "medium",
      "A and B can complete a work in 15 days and 10 days respectively. They started together, but B left after 2 days. In how many days will A finish the remaining work?",
      ["10 days", "11 days", "12 days", "13 days"], 0,
      "In 2 days, together work = 2 * (1/15 + 1/10) = 2 * (5/30) = 1/3. Remaining = 2/3. Time for A = (2/3) / (1/15) = 10 days.",
      "Compute work completed during the 2 joint days, then find remaining work for A.",
      "Work done = 2/6 = 1/3. Remaining = 2/3. A's time = (2/3) * 15 = 10 days.")

add_q("Quantitative", "Ratio & Proportion", "medium",
      "A sum of $750 is divided among A, B, and C such that A : B = 2 : 3 and B : C = 6 : 5. How much does A receive?",
      ["$180", "$200", "$240", "$250"], 1,
      "A : B : C = 4 : 6 : 5. Total parts = 15 parts = $750 => 1 part = $50. A = 4 * 50 = $200.",
      "Combine ratios to find A:B:C.",
      "A:B:C = 4:6:5. A's share = 4/15 of 750 = 200.")

add_q("Quantitative", "Average", "medium",
      "The average monthly income of P and Q is $5,050, Q and R is $6,250, and P and R is $5,200. Find P's monthly income.",
      ["$4,000", "$4,200", "$4,500", "$5,000"], 0,
      "P+Q = 10,100; Q+R = 12,500; P+R = 10,400. 2(P+Q+R) = 33,000 => P+Q+R = 16,500. P = 16,500 - 12,500 = $4,000.",
      "Sum all three equations to get 2(P + Q + R), then subtract (Q + R).",
      "(10100 + 12500 + 10400)/2 - 12500 = 16500 - 12500 = 4000.")

# --- 12 Hard Quantitative ---
add_q("Quantitative", "Profit & Loss", "hard",
      "A shopkeeper marks an article 40% above cost and offers a 15% discount. If his net profit is $133, what was the original cost price?",
      ["$650", "$700", "$750", "$800"], 1,
      "CP = 100x. MP = 140x. SP = 140x * 0.85 = 119x. Profit = 19x = 133 => x = 7. CP = $700.",
      "Express MP and SP in terms of CP, then equate (SP - CP) to $133.",
      "1.40 * 0.85 = 1.19. Profit is 0.19 * CP = 133. CP = 133 / 0.19 = 700.")

add_q("Quantitative", "Numbers", "hard",
      "Find the remainder when 7^84 is divided by 342.",
      ["1", "7", "49", "341"], 0,
      "7^3 = 343 = 342 + 1 ≡ 1 (mod 342). 7^84 = (7^3)^28 ≡ (1)^28 = 1.",
      "Observe that 7^3 = 343 is 1 greater than 342.",
      "Use modular equivalence: (343)^28 ≡ 1^28 mod 342.")

add_q("Quantitative", "Mixture & Alligation", "hard",
      "A vessel contains 80L pure milk. 20L is replaced with water twice. What is the final quantity of milk left?",
      ["42L", "45L", "48L", "50L"], 1,
      "Final milk = 80 * (1 - 20/80)^2 = 80 * (3/4)^2 = 80 * 9/16 = 45L.",
      "Use successive dilution formula: Initial * (1 - x/V)^n.",
      "80 * (3/4)^2 = 80 * 9/16 = 45L.")

add_q("Quantitative", "Time & Work", "hard",
      "A and B can complete a work in 12 and 18 days. A works alone for 4 days, then B joins. In how many total days is the work finished?",
      ["8.8 days", "9.6 days", "10.2 days", "11.4 days"], 0,
      "A in 4 days = 4/12 = 1/3. Remaining = 2/3. Together rate = 5/36. Joint time = (2/3)/(5/36) = 4.8. Total = 4 + 4.8 = 8.8 days.",
      "Calculate work left after A's 4 days, then divide by combined efficiency.",
      "Remaining is 2/3. (2/3) / (5/36) = 24/5 = 4.8. Total = 4 + 4.8 = 8.8.")

add_q("Quantitative", "Permutation & Combination", "hard",
      "In how many ways can the letters of 'CORPORATION' be arranged such that all vowels always come together?",
      ["4,800", "7,200", "14,400", "50,400"], 3,
      "Vowels are O, O, A, I, O (5 vowels: 3 O's). Consonants: C, R, P, R, T, N (6 consonants: 2 R's). Units = 6 + 1 = 7. Ways = (7!/2!) * (5!/3!) = 2520 * 20 = 50,400.",
      "Group all vowels into a single composite block.",
      "Arrange 7 units with 2 R's: 7!/2!. Arrange vowels inside block with 3 O's: 5!/3!. Multiply both.")

add_q("Quantitative", "Numbers", "hard",
      "What is the highest power of 7 that divides 1000! completely?",
      ["160", "164", "168", "172"], 1,
      "Legendre's Formula: [1000/7] + [1000/49] + [1000/343] = 142 + 20 + 2 = 164.",
      "Sum the integer quotients of 1000 divided by successive powers of 7.",
      "142 + 20 + 2 = 164.")

add_q("Quantitative", "Algebra", "hard",
      "If x + 1/x = 4, what is the value of x^5 + 1/x^5?",
      ["724", "726", "728", "732"], 0,
      "(x^2 + 1/x^2) = 14; (x^3 + 1/x^3) = 52. (14 * 52) - 4 = 728 - 4 = 724.",
      "Multiply (x^2 + 1/x^2) by (x^3 + 1/x^3) and subtract (x + 1/x).",
      "14 * 52 - 4 = 724.")

add_q("Quantitative", "Time, Speed & Distance", "hard",
      "A boat travels 24 km upstream and 36 km downstream in 6 hours. It also travels 36 km upstream and 24 km downstream in 6.5 hours. Find current speed.",
      ["1.5 km/h", "2 km/h", "2.5 km/h", "3 km/h"], 1,
      "Solving simultaneous equations gives Upstream speed = 8 km/h, Downstream speed = 12 km/h. Current = (12 - 8)/2 = 2 km/h.",
      "Let 1/u and 1/v be variables and set up two linear equations.",
      "Upstream = 8, Downstream = 12. Current = (v - u)/2.")

add_q("Quantitative", "Probability", "hard",
      "Three urns contain: Urn I (3W, 2B), Urn II (2W, 3B), Urn III (4W, 1B). An urn is picked and a ball drawn is White. Probability it was from Urn I?",
      ["1/3", "1/4", "3/8", "2/5"], 0,
      "P(U) = 1/3 each. P(W) = (1/3)(3/5 + 2/5 + 4/5) = 3/5. P(U1|W) = (1/3 * 3/5) / (3/5) = 1/3.",
      "Apply Bayes' theorem: P(U1|W) = P(U1 and W) / P(W).",
      "P(U1 and W) = 1/5. P(W) = 3/5. Ratio = (1/5) / (3/5) = 1/3.")

add_q("Quantitative", "Percentages", "hard",
      "A sum invested at compound interest doubles in 5 years. In how many years will it become 16 times its original amount?",
      ["15 years", "20 years", "25 years", "30 years"], 1,
      "16 = 2^4. Time required = 4 * 5 = 20 years.",
      "Express 16 as a power of 2: 16 = 2^k.",
      "k = 4, so time = 4 * 5 = 20 years.")

add_q("Quantitative", "Mensuration", "hard",
      "The slant height of a right circular cone is 25 cm and its height is 24 cm. Find its curved surface area (use pi = 22/7).",
      ["528 cm^2", "550 cm^2", "572 cm^2", "600 cm^2"], 1,
      "Radius r = sqrt(25^2 - 24^2) = 7 cm. CSA = pi * r * l = (22/7) * 7 * 25 = 550 cm^2.",
      "Calculate base radius using Pythagorean theorem r = sqrt(l^2 - h^2).",
      "r = 7 cm. Area = (22/7) * 7 * 25 = 550 cm^2.")

add_q("Quantitative", "Progression", "hard",
      "Find the sum of all two-digit numbers which leave a remainder of 3 when divided by 7.",
      ["676", "689", "702", "715"], 0,
      "Numbers: 10, 17, 24, ..., 94 (13 terms). Sum = (13/2)(10 + 94) = 13 * 52 = 676.",
      "Identify the first (10) and last (94) numbers and use the AP sum formula.",
      "n = (94-10)/7 + 1 = 13. Sum = 13 * (10 + 94)/2 = 676.")

print(f"Total Quantitative: {len([q for q in questions if q['category'] == 'Quantitative'])}")

# Write temporary progress to avoid giant single file

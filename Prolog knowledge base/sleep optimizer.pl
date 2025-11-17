% Sleep Quality Optimizer Expert System in Prolog

:- dynamic fact/2.

% ==================== MAIN DIAGNOSIS PREDICATE ====================

diagnose :-
    retractall(diagnosis(_,_)),
    retractall(recommendation(_,_)),
    write('=== Sleep Quality Optimizer Expert System ==='), nl, nl,
    collect_user_input,
    nl,
    write('=== ANALYSIS RESULTS ==='), nl, nl,
    findall(_, apply_rules, _),
    display_results,
    nl,
    write('Would you like to diagnose again? (yes/no): '),
    read(Response),
    (Response = yes -> retractall(fact(_,_)), nl, diagnose ;
     write('Thank you for using the Sleep Quality Optimizer!'), nl).

% ==================== USER INPUT COLLECTION ====================

collect_user_input :-
    write('Please answer the following questions:'), nl, nl,

    ask('How would you rate your sleep quality? (good/poor/fair)', sleep_quality),
    ask('How long is your sleep duration? (adequate/insufficient)', sleep_duration),
    ask('How is your daytime sleepiness? (low/high/moderate)', daytime_sleepiness),
    ask('How loud is your snoring? (none/moderate/loud)', snoring),
    ask('Do you experience breathing pauses? (yes/no)', breathing_pauses),
    ask('How long does it take to fall asleep? (short/long)', sleep_onset),
    ask('When do you consume caffeine? (early/late/none)', caffeine_timing),
    ask('How much screen time before bed? (low/high)', screen_time),
    ask('How frequent are night awakenings? (rare/frequent)', night_awakenings),
    ask('Do you have racing thoughts? (yes/no)', racing_thoughts),
    ask('What is your stress level? (low/high/moderate)', stress_level),
    ask('Do you consume alcohol before bed? (yes/no)', alcohol_consumption),
    ask('How consistent is your sleep schedule? (good/poor)', schedule_consistency),
    ask('Do you work shifts? (yes/no)', shift_work),
    ask('Is your bedtime irregular? (yes/no)', irregular_bedtime),
    ask('Do you have leg discomfort at night? (yes/no)', leg_discomfort),
    ask('Do you have urge to move legs? (yes/no)', urge_to_move),
    ask('What is your room temperature? (comfortable/too_hot/too_cold)', room_temp),
    ask('How is the bedroom light? (dark/bright)', bedroom_light),
    ask('How is the bedroom noise level? (low/high)', bedroom_noise),
    ask('Do you use bedroom for multiple activities? (sleep_only/multiple)', bedroom_activities),
    ask('When do you exercise? (morning/afternoon/late/none)', exercise_timing),
    ask('When do you eat meals? (early/late)', meal_timing),
    ask('How much do you nap? (none/moderate/excessive)', napping),
    ask('What is your anxiety level? (low/high/moderate)', anxiety).

ask(Question, Attribute) :-
    format('~w~n> ', [Question]),
    read(Answer),
    assert(fact(Attribute, Answer)).

% ==================== KNOWLEDGE BASE - DIAGNOSIS RULES ====================

% Sleep Apnea - Severe
apply_rules :-
    fact(snoring, loud),
    fact(breathing_pauses, yes),
    fact(daytime_sleepiness, high),
    \+ diagnosis('Possible Sleep Apnea (High Risk)', _),
    assert(diagnosis('Possible Sleep Apnea (High Risk)', 0.85)),
    assert(recommendation('URGENT: Consult a sleep specialist immediately', high)),
    assert(recommendation('Sleep apnea can be serious and requires medical evaluation', high)),
    fail.

% Sleep Apnea - Moderate
apply_rules :-
    fact(snoring, loud),
    (fact(breathing_pauses, yes) ; fact(daytime_sleepiness, high)),
    \+ diagnosis('Possible Sleep Apnea (Moderate Risk)', _),
    assert(diagnosis('Possible Sleep Apnea (Moderate Risk)', 0.65)),
    assert(recommendation('Consider consulting a sleep specialist', medium)),
    assert(recommendation('Monitor symptoms and keep a sleep diary', medium)),
    fail.

% Caffeine-Related Insomnia
apply_rules :-
    fact(sleep_onset, long),
    fact(caffeine_timing, late),
    \+ diagnosis('Caffeine-Related Onset Insomnia', _),
    assert(diagnosis('Caffeine-Related Onset Insomnia', 0.75)),
    assert(recommendation('Avoid caffeine after 2 PM', high)),
    assert(recommendation('Switch to decaf or herbal tea in afternoon/evening', medium)),
    fail.

% Blue Light-Related Insomnia
apply_rules :-
    fact(sleep_onset, long),
    fact(screen_time, high),
    \+ diagnosis('Blue Light-Related Onset Insomnia', _),
    assert(diagnosis('Blue Light-Related Onset Insomnia', 0.70)),
    assert(recommendation('Limit screen time 1-2 hours before bed', high)),
    assert(recommendation('Use blue light filters or night mode on devices', medium)),
    assert(recommendation('Try reading a physical book instead', low)),
    fail.

% Stress-Related Insomnia
apply_rules :-
    fact(night_awakenings, frequent),
    fact(racing_thoughts, yes),
    fact(stress_level, high),
    \+ diagnosis('Stress-Related Maintenance Insomnia', _),
    assert(diagnosis('Stress-Related Maintenance Insomnia', 0.80)),
    assert(recommendation('Practice relaxation techniques (deep breathing, meditation)', high)),
    assert(recommendation('Consider cognitive behavioral therapy for insomnia (CBT-I)', high)),
    assert(recommendation('Keep a worry journal - write down concerns before bed', medium)),
    assert(recommendation('Try progressive muscle relaxation', low)),
    fail.

% Alcohol-Disrupted Sleep
apply_rules :-
    fact(night_awakenings, frequent),
    fact(alcohol_consumption, yes),
    \+ diagnosis('Alcohol-Disrupted Sleep', _),
    assert(diagnosis('Alcohol-Disrupted Sleep', 0.75)),
    assert(recommendation('Avoid alcohol 3-4 hours before bedtime', high)),
    assert(recommendation('Alcohol disrupts REM sleep and causes frequent awakenings', medium)),
    fail.

% Circadian Rhythm Disruption
apply_rules :-
    fact(schedule_consistency, poor),
    (fact(shift_work, yes) ; fact(irregular_bedtime, yes)),
    \+ diagnosis('Circadian Rhythm Disruption', _),
    assert(diagnosis('Circadian Rhythm Disruption', 0.70)),
    assert(recommendation('Establish consistent sleep/wake times (even on weekends)', high)),
    assert(recommendation('Get bright light exposure in the morning', high)),
    assert(recommendation('Avoid bright light 2-3 hours before bed', medium)),
    assert(recommendation('Consider light therapy if working shifts', medium)),
    fail.

% Restless Leg Syndrome
apply_rules :-
    fact(leg_discomfort, yes),
    fact(urge_to_move, yes),
    \+ diagnosis('Possible Restless Leg Syndrome', _),
    assert(diagnosis('Possible Restless Leg Syndrome', 0.80)),
    assert(recommendation('Consult a physician for proper diagnosis', high)),
    assert(recommendation('Check iron and magnesium levels', high)),
    assert(recommendation('Try leg massages or stretching before bed', medium)),
    assert(recommendation('Avoid caffeine which can worsen symptoms', medium)),
    fail.

% Environmental Temperature Issue
apply_rules :-
    (fact(room_temp, too_hot) ; fact(room_temp, too_cold)),
    \+ diagnosis('Environmental Temperature Issue', _),
    assert(diagnosis('Environmental Temperature Issue', 0.65)),
    assert(recommendation('Keep bedroom temperature between 60-67°F (15-19°C)', high)),
    assert(recommendation('Use breathable bedding materials', medium)),
    assert(recommendation('Consider a fan or adjust heating/cooling', medium)),
    fail.

% Light Pollution
apply_rules :-
    fact(bedroom_light, bright),
    \+ diagnosis('Light Pollution Affecting Sleep', _),
    assert(diagnosis('Light Pollution Affecting Sleep', 0.70)),
    assert(recommendation('Use blackout curtains or eye mask', high)),
    assert(recommendation('Remove or cover LED lights from devices', medium)),
    assert(recommendation('Use dim red lights if nightlight needed', low)),
    fail.

% Noise Disruption
apply_rules :-
    fact(bedroom_noise, high),
    \+ diagnosis('Noise-Related Sleep Disruption', _),
    assert(diagnosis('Noise-Related Sleep Disruption', 0.65)),
    assert(recommendation('Use white noise machine or fan', high)),
    assert(recommendation('Try earplugs designed for sleeping', medium)),
    assert(recommendation('Address noise sources if possible', medium)),
    fail.

% Poor Sleep Hygiene
apply_rules :-
    fact(sleep_onset, long),
    fact(bedroom_activities, multiple),
    \+ diagnosis('Poor Sleep Hygiene - Bedroom Association', _),
    assert(diagnosis('Poor Sleep Hygiene - Bedroom Association', 0.70)),
    assert(recommendation('Use bedroom only for sleep and intimacy', high)),
    assert(recommendation('Remove TV, work materials from bedroom', high)),
    assert(recommendation('If can\'t sleep after 20 min, leave bedroom until sleepy', medium)),
    fail.

% Late Exercise
apply_rules :-
    fact(exercise_timing, late),
    \+ diagnosis('Exercise-Related Sleep Disruption', _),
    assert(diagnosis('Exercise-Related Sleep Disruption', 0.60)),
    assert(recommendation('Avoid vigorous exercise 3-4 hours before bed', high)),
    assert(recommendation('Try morning or afternoon exercise instead', medium)),
    assert(recommendation('Gentle stretching or yoga in evening is okay', low)),
    fail.

% Late Meals
apply_rules :-
    fact(meal_timing, late),
    \+ diagnosis('Meal Timing Affecting Sleep', _),
    assert(diagnosis('Meal Timing Affecting Sleep', 0.60)),
    assert(recommendation('Avoid large meals 2-3 hours before bed', high)),
    assert(recommendation('If hungry, try light snack (banana, milk)', medium)),
    assert(recommendation('Avoid spicy or acidic foods in evening', medium)),
    fail.

% Excessive Napping
apply_rules :-
    fact(napping, excessive),
    \+ diagnosis('Excessive Daytime Napping', _),
    assert(diagnosis('Excessive Daytime Napping', 0.65)),
    assert(recommendation('Limit naps to 20-30 minutes', high)),
    assert(recommendation('Avoid napping after 3 PM', high)),
    assert(recommendation('If very sleepy, investigate underlying causes', medium)),
    fail.

% Sleep Deprivation
apply_rules :-
    fact(sleep_duration, insufficient),
    fact(daytime_sleepiness, high),
    \+ diagnosis('Chronic Sleep Deprivation', _),
    assert(diagnosis('Chronic Sleep Deprivation', 0.80)),
    assert(recommendation('Prioritize 7-9 hours of sleep per night', high)),
    assert(recommendation('Gradually adjust bedtime earlier by 15 min increments', high)),
    assert(recommendation('Evaluate and reduce time-wasting activities', medium)),
    fail.

% Anxiety-Related Sleep Issues
apply_rules :-
    fact(anxiety, high),
    (fact(sleep_onset, long) ; fact(night_awakenings, frequent)),
    \+ diagnosis('Anxiety-Related Sleep Disturbance', _),
    assert(diagnosis('Anxiety-Related Sleep Disturbance', 0.75)),
    assert(recommendation('Consider therapy or counseling for anxiety', high)),
    assert(recommendation('Practice mindfulness meditation', high)),
    assert(recommendation('Try 4-7-8 breathing technique', medium)),
    assert(recommendation('Avoid checking clock during night', medium)),
    fail.

% Healthy Sleep Pattern
apply_rules :-
    fact(sleep_quality, good),
    fact(sleep_duration, adequate),
    fact(daytime_sleepiness, low),
    \+ diagnosis('Healthy Sleep Pattern', _),
    assert(diagnosis('Healthy Sleep Pattern', 0.90)),
    assert(recommendation('Your sleep appears healthy - maintain current habits!', low)),
    assert(recommendation('Continue consistent sleep schedule', low)),
    fail.
% Insufficient Information
apply_rules :-
    \+ fact(sleep_quality, good),
    \+ fact(sleep_quality, poor),
    \+ diagnosis('Insufficient Information', _),
    assert(diagnosis('Insufficient Information', 0.50)),
    assert(recommendation('Keep a detailed sleep diary for 2 weeks', high)),
    assert(recommendation('Track bedtime, wake time, and sleep quality', high)),
    assert(recommendation('Note factors like caffeine, exercise, stress', medium)),
    fail.
apply_rules.

% ==================== DISPLAY RESULTS ====================

display_results :-
    write('DIAGNOSES:'), nl,
    write('----------'), nl,
    (diagnosis(_, _) ->
        forall(diagnosis(D, Conf),
               format('- ~w (Confidence: ~2f)~n', [D, Conf]))
    ;
        write('No specific diagnosis identified.'), nl
    ),
    nl,
    write('RECOMMENDATIONS:'), nl,
    write('----------------'), nl,
    (recommendation(_, _) ->
        (write('High Priority:'), nl,
         forall(recommendation(R, high), format('  * ~w~n', [R])),
         nl,
         write('Medium Priority:'), nl,
         forall(recommendation(R, medium), format('  * ~w~n', [R])),
         nl,
         write('Low Priority:'), nl,
         forall(recommendation(R, low), format('  * ~w~n', [R])))
    ;
        write('No specific recommendations.'), nl
    ).

% ==================== HELPER PREDICATES ====================

:- dynamic diagnosis/2.
:- dynamic recommendation/2.

% Quick diagnosis with predefined facts (for testing)
quick_test :-
    retractall(fact(_,_)),
    retractall(diagnosis(_,_)),
    retractall(recommendation(_,_)),

    % Sample test case: Person with sleep apnea symptoms
    assert(fact(sleep_quality, poor)),
    assert(fact(snoring, loud)),
    assert(fact(breathing_pauses, yes)),
    assert(fact(daytime_sleepiness, high)),
    assert(fact(sleep_duration, insufficient)),
    assert(fact(caffeine_timing, early)),
    assert(fact(screen_time, low)),

    write('=== Running Quick Test ==='), nl, nl,
    findall(_, apply_rules, _),
    display_results.


% Test case for insufficient information rule
test_insufficient_info :-
    retractall(fact(_,_)),
    retractall(diagnosis(_,_)),
    retractall(recommendation(_,_)),

    % Person answers "fair" for sleep quality
    assert(fact(sleep_quality, fair)),
    assert(fact(sleep_duration, adequate)),
    assert(fact(daytime_sleepiness, moderate)),

    write('=== Testing Insufficient Information Rule ==='), nl, nl,
    findall(_, apply_rules, _),
    display_results.

% Start message
:- write('Sleep Quality Optimizer Expert System loaded.'), nl,
   write('Type "diagnose." to start the diagnosis.'), nl,
   write('Type "quick_test." to run a sample diagnosis.'), nl, nl.

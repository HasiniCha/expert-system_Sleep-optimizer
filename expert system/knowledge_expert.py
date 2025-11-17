from experta import *

class SleepFact(Fact):
    """Fact to store sleep-related information"""
    pass

class SleepQualityOptimizer(KnowledgeEngine):
    """Expert system for diagnosing sleep issues and providing recommendations"""
    
    def __init__(self):
        super().__init__()
        self.diagnoses = []
        self.recommendations = []
        self.confidence_scores = {}
    
    def reset_results(self):
        """Reset diagnoses and recommendations"""
        self.diagnoses = []
        self.recommendations = []
        self.confidence_scores = {}
    
    # ==================== SLEEP APNEA RULES ====================
    
    @Rule(SleepFact(snoring='loud'),
          SleepFact(breathing_pauses='yes'),
          SleepFact(daytime_sleepiness='high'))
    def sleep_apnea_severe(self):
        diagnosis = "Possible Sleep Apnea (High Risk)"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.85
        self.recommendations.append(("URGENT: Consult a sleep specialist immediately", "high"))
        self.recommendations.append(("Sleep apnea can be serious and requires medical evaluation", "high"))
    
    @Rule(SleepFact(snoring='loud'),
          OR(SleepFact(breathing_pauses='yes'),
             SleepFact(daytime_sleepiness='high')))
    def sleep_apnea_moderate(self):
        diagnosis = "Possible Sleep Apnea (Moderate Risk)"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.65
        self.recommendations.append(("Consider consulting a sleep specialist", "medium"))
        self.recommendations.append(("Monitor symptoms and keep a sleep diary", "medium"))
    
    # ==================== INSOMNIA RULES ====================
    
    @Rule(SleepFact(sleep_onset='long'),
          SleepFact(caffeine_timing='late'))
    def caffeine_insomnia(self):
        diagnosis = "Caffeine-Related Onset Insomnia"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.75
        self.recommendations.append(("Avoid caffeine after 2 PM", "high"))
        self.recommendations.append(("Switch to decaf or herbal tea in afternoon/evening", "medium"))
    
    @Rule(SleepFact(sleep_onset='long'),
          SleepFact(screen_time='high'))
    def screen_insomnia(self):
        diagnosis = "Blue Light-Related Onset Insomnia"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.70
        self.recommendations.append(("Limit screen time 1-2 hours before bed", "high"))
        self.recommendations.append(("Use blue light filters or night mode on devices", "medium"))
        self.recommendations.append(("Try reading a physical book instead", "low"))
    
    @Rule(SleepFact(night_awakenings='frequent'),
          SleepFact(racing_thoughts='yes'),
          SleepFact(stress_level='high'))
    def stress_insomnia(self):
        diagnosis = "Stress-Related Maintenance Insomnia"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.80
        self.recommendations.append(("Practice relaxation techniques (deep breathing, meditation)", "high"))
        self.recommendations.append(("Consider cognitive behavioral therapy for insomnia (CBT-I)", "high"))
        self.recommendations.append(("Keep a worry journal - write down concerns before bed", "medium"))
        self.recommendations.append(("Try progressive muscle relaxation", "low"))
    
    @Rule(SleepFact(night_awakenings='frequent'),
          SleepFact(alcohol_consumption='yes'))
    def alcohol_disruption(self):
        diagnosis = "Alcohol-Disrupted Sleep"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.75
        self.recommendations.append(("Avoid alcohol 3-4 hours before bedtime", "high"))
        self.recommendations.append(("Alcohol disrupts REM sleep and causes frequent awakenings", "medium"))
    
    # ==================== CIRCADIAN RHYTHM RULES ====================
    
    @Rule(SleepFact(schedule_consistency='poor'),
          OR(SleepFact(shift_work='yes'),
             SleepFact(irregular_bedtime='yes')))
    def circadian_disruption(self):
        diagnosis = "Circadian Rhythm Disruption"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.70
        self.recommendations.append(("Establish consistent sleep/wake times (even on weekends)", "high"))
        self.recommendations.append(("Get bright light exposure in the morning", "high"))
        self.recommendations.append(("Avoid bright light 2-3 hours before bed", "medium"))
        self.recommendations.append(("Consider light therapy if working shifts", "medium"))
    
    # ==================== RESTLESS LEG SYNDROME ====================
    
    @Rule(SleepFact(leg_discomfort='yes'),
          SleepFact(urge_to_move='yes'))
    def restless_leg_syndrome(self):
        diagnosis = "Possible Restless Leg Syndrome"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.80
        self.recommendations.append(("Consult a physician for proper diagnosis", "high"))
        self.recommendations.append(("Check iron and magnesium levels", "high"))
        self.recommendations.append(("Try leg massages or stretching before bed", "medium"))
        self.recommendations.append(("Avoid caffeine which can worsen symptoms", "medium"))
    
    # ==================== ENVIRONMENTAL RULES ====================
    
    @Rule(OR(SleepFact(room_temp='too_hot'),
             SleepFact(room_temp='too_cold')))
    def temperature_issue(self):
        diagnosis = "Environmental Temperature Issue"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.65
        self.recommendations.append(("Keep bedroom temperature between 60-67°F (15-19°C)", "high"))
        self.recommendations.append(("Use breathable bedding materials", "medium"))
        self.recommendations.append(("Consider a fan or adjust heating/cooling", "medium"))
    
    @Rule(SleepFact(bedroom_light='bright'))
    def light_pollution(self):
        diagnosis = "Light Pollution Affecting Sleep"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.70
        self.recommendations.append(("Use blackout curtains or eye mask", "high"))
        self.recommendations.append(("Remove or cover LED lights from devices", "medium"))
        self.recommendations.append(("Use dim red lights if nightlight needed", "low"))
    
    @Rule(SleepFact(bedroom_noise='high'))
    def noise_disruption(self):
        diagnosis = "Noise-Related Sleep Disruption"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.65
        self.recommendations.append(("Use white noise machine or fan", "high"))
        self.recommendations.append(("Try earplugs designed for sleeping", "medium"))
        self.recommendations.append(("Address noise sources if possible", "medium"))
    
    # ==================== POOR SLEEP HYGIENE ====================
    
    @Rule(SleepFact(sleep_onset='long'),
          SleepFact(bedroom_activities='multiple'))
    def poor_sleep_hygiene(self):
        diagnosis = "Poor Sleep Hygiene - Bedroom Association"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.70
        self.recommendations.append(("Use bedroom only for sleep and intimacy", "high"))
        self.recommendations.append(("Remove TV, work materials from bedroom", "high"))
        self.recommendations.append(("If can't sleep after 20 min, leave bedroom until sleepy", "medium"))
    
    @Rule(SleepFact(exercise_timing='late'))
    def late_exercise(self):
        diagnosis = "Exercise-Related Sleep Disruption"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.60
        self.recommendations.append(("Avoid vigorous exercise 3-4 hours before bed", "high"))
        self.recommendations.append(("Try morning or afternoon exercise instead", "medium"))
        self.recommendations.append(("Gentle stretching or yoga in evening is okay", "low"))
    
    @Rule(SleepFact(meal_timing='late'))
    def late_meals(self):
        diagnosis = "Meal Timing Affecting Sleep"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.60
        self.recommendations.append(("Avoid large meals 2-3 hours before bed", "high"))
        self.recommendations.append(("If hungry, try light snack (banana, milk)", "medium"))
        self.recommendations.append(("Avoid spicy or acidic foods in evening", "medium"))
    
    @Rule(SleepFact(napping='excessive'))
    def excessive_napping(self):
        diagnosis = "Excessive Daytime Napping"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.65
        self.recommendations.append(("Limit naps to 20-30 minutes", "high"))
        self.recommendations.append(("Avoid napping after 3 PM", "high"))
        self.recommendations.append(("If very sleepy, investigate underlying causes", "medium"))
    
    # ==================== GENERAL SLEEP DEPRIVATION ====================
    
    @Rule(SleepFact(sleep_duration='insufficient'),
          SleepFact(daytime_sleepiness='high'))
    def sleep_deprivation(self):
        diagnosis = "Chronic Sleep Deprivation"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.80
        self.recommendations.append(("Prioritize 7-9 hours of sleep per night", "high"))
        self.recommendations.append(("Gradually adjust bedtime earlier by 15 min increments", "high"))
        self.recommendations.append(("Evaluate and reduce time-wasting activities", "medium"))
    
    # ==================== ANXIETY/MENTAL HEALTH ====================
    
    @Rule(SleepFact(anxiety='high'),
          OR(SleepFact(sleep_onset='long'),
             SleepFact(night_awakenings='frequent')))
    def anxiety_sleep_issues(self):
        diagnosis = "Anxiety-Related Sleep Disturbance"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.75
        self.recommendations.append(("Consider therapy or counseling for anxiety", "high"))
        self.recommendations.append(("Practice mindfulness meditation", "high"))
        self.recommendations.append(("Try 4-7-8 breathing technique", "medium"))
        self.recommendations.append(("Avoid checking clock during night", "medium"))
    
    # ==================== POSITIVE SLEEP PATTERNS ====================
    
    @Rule(SleepFact(sleep_quality='good'),
          SleepFact(sleep_duration='adequate'),
          SleepFact(daytime_sleepiness='low'))
    def healthy_sleep(self):
        diagnosis = "Healthy Sleep Pattern"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.90
        self.recommendations.append(("Your sleep appears healthy - maintain current habits!", "low"))
        self.recommendations.append(("Continue consistent sleep schedule", "low"))
    
    # ==================== NO CLEAR DIAGNOSIS ====================
    
    @Rule(AND(~SleepFact(sleep_quality='good'),
              ~SleepFact(sleep_quality='poor')))
    def insufficient_information(self):
        diagnosis = "Insufficient Information"
        self.diagnoses.append(diagnosis)
        self.confidence_scores[diagnosis] = 0.50
        self.recommendations.append(("Keep a detailed sleep diary for 2 weeks", "high"))
        self.recommendations.append(("Track bedtime, wake time, and sleep quality", "high"))
        self.recommendations.append(("Note factors like caffeine, exercise, stress", "medium"))

def run_diagnosis(user_inputs):
    """
    Run the expert system with user inputs
    
    Args:
        user_inputs: Dictionary of user responses
    
    Returns:
        Tuple of (diagnoses, recommendations, confidence_scores)
    """
    engine = SleepQualityOptimizer()
    engine.reset()
    engine.reset_results()
    
    # Declare facts based on user inputs
    for key, value in user_inputs.items():
        engine.declare(SleepFact(**{key: value}))
    
    # Run the inference engine
    engine.run()
    
    return engine.diagnoses, engine.recommendations, engine.confidence_scores
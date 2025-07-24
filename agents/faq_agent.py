import re
from difflib import get_close_matches

# Predefined NuGenomics FAQ data
FAQ_DATA = {
    "What is NuGenomics?": "NuGenomics is a DNA‑based wellness platform offering personalised health insights.",
    "How does genetic testing help with weight management?": "It analyses your genes to personalise nutrition and fitness strategies for better weight management.",
    "What makes the DNA weight management program unique?": "Our program combines genetic analysis with lifestyle coaching to make weight loss faster, more sustainable and tailored to you.",
    "How do I take the DNA test?": "You’ll receive a saliva‑based home collection kit. Just register it online and send it back using the prepaid envelope.",
    "How long to get results?": "Results are sent via email within 2‑3 weeks after the lab receives your sample.",
    "Is my data private?": "Yes! We use encrypted storage and follow strict privacy policies; your data is never shared without your consent.",
    "Can I get a consultation after results?": "Yes, you can schedule a consultation with our wellness experts after receiving your results.",
    "What is the cost of the testing program?": "Prices vary by program, but our DNA‑based weight and wellness testing start from ₹5,999. Visit our pricing page for details.",
    "Can I upgrade after testing?": "Yes, you can purchase additional tests or coaching packages any time via our portal.",
    "How do I cancel or request a refund?": "Please see our refund policy or contact support@nugenomics.in for assistance.",
    "Who is the program for?":
        "This program is for everyone—from under 20 to over 70. It adapts to your age, lifestyle and eating habits to optimize your current and future health.",
    
    "And how does it work?":
        "We analyse your DNA (‘source code’), combine it with your blood test results, medical history and lifestyle data, then create a personalized, bite-sized health plan with pre- and post-counselling sessions.",
    
    "Will you be telling me what to eat & what not to?":
        "Yes and no. There are nutritional interventions personalized to your genetic and lifestyle profile, but no starvation—we design plans that are sustainable and balanced.",
    
    "Am I going to need to go get a gym membership?":
        "Not at all. We may include light exercises as needed, all of which can be done without a gym. As always, consult your physician before making changes.",
    
    "What do you aim to provide with this program?":
        "Optimal health – boosting immunity, energy, strength, and metabolism, and reducing body fat, inflammation, skin issues and allergies.",
    
    "What’s the difference between this and any other health & wellness program?":
        "It’s holistic, science-based, personalized using your DNA and blood insights, with small sustainable changes, not magic or extreme routines.",
    
    "You test my blood. Will you help bring all the stats in line?":
        "Yes. We test over 70 blood parameters, pinpoint deviations, and recommend changes to get your metrics back on track through nutrition and lifestyle.",
    
    "What are the genetic parameters you consider during sample testing?":
        "We analyse metabolic health (blood sugar, cholesterol, HDL, LDL), nutritional status, food sensitivities (e.g. wheat, caffeine), ageing markers and addiction susceptibility.",
    
    "How does genetic information help personalize my program?":
        "Your DNA helps eliminate guesswork: it shows your macro/micronutrient needs, intolerances, and predicted food responses—enabling truly personalized planning.",
    
    "What degree of fitness do you expect from me?":
        "We start where you are now and aim for long-term holistic improvement; there's no preset fitness requirement—but always follow physician guidelines.",
    
    "How long does this program usually last?":
        "The initial plan runs for 3 months to kickstart your health goals. After that, you can continue with monthly, quarterly, half-yearly or yearly subscriptions.",
    
    "What does the initial 3-month plan provide?":
        "It includes a genomic test, a 70+ blood parameter report, pre- and post-counselling sessions, and an actionable health plan tailored to you.",
    
    "After these initial 3-months, what are your subscription options?":
        "You can continue with monthly, quarterly, half-yearly or annual subscription plans based on your needs.",
    
    "Do I have to pay all at once or do you have EMIs?":
        "Yes, EMI options are available on select credit and debit cards.",
    
    "Are you up to date with data & information security norms?":
        "Yes, we comply with GDPR and India's Data Protection Bill 2019. Your data is anonymized, encrypted, and separated from your personal identity.",
    
    "Will my results indicate any medical or diagnostic info?":
        "No, the tests are for predictive and preventive purposes, not medical diagnosis. Please consult your doctor for any health issues.",
    
    "Just out of curiosity, do you think you can really determine your health and fitness based on your DNA?":
        "Yes. We combine your DNA with environmental and lifestyle data to design personalized wellness plans backed by science.",
    
    "Once we’re done, I’d like you to get rid of my sample. Would that be possible?":
        "Yes, your physical sample is yours. You can request its destruction and deletion of your data; future products will need retesting.",
    
    "What about my personal information from your systems?":
        "Yes. You have full control. If you choose to delete your information, all your test results and medical records will be permanently erased from our systems. If you keep it, you can access future products without re-testing.",
    
    "Can I reschedule my Genetic Counselling session?":
        "Yes, you can reschedule it twice. After that, a ₹500 fee applies. Please inform support at least 24 hours in advance.",
    
    "Can I reschedule my Lifestyle Analysis session?":
        "Yes, you can reschedule it twice. After that, a ₹500 fee applies. Please inform support at least 24 hours in advance.",
    
    "Can I reschedule my wellbeing and transformation session?":
        "Yes, you can reschedule it twice. After that, a ₹300 fee applies. Please inform support at least 24 hours in advance.",
    
    "Can I reschedule my sample collection?":
        "Yes, you can reschedule it up to 3 times, at least 24 hours before the appointment. After that, contact support.",
    
    "What is a wellbeing and transformation session?":
        "These are sessions with our mental health experts to help address any emotional or mental roadblocks during your program.",
    
    "When will I get my Blood report?":
        "Your blood report will be ready within 72 hours after sample collection."
}



def clean_text(text):
    """Lowercase and remove punctuation for better matching."""
    return re.sub(r"[^\w\s]", "", text.lower())

def get_faq_answer(query):
    """Return the best-matched answer from FAQ_DATA."""
    query_c = clean_text(query)

    # Exact keyword presence matching
    for q, a in FAQ_DATA.items():
        if all(word in clean_text(q) for word in query_c.split()):
            return a

    # Fuzzy match with cutoff
    questions = list(FAQ_DATA.keys())
    matches = get_close_matches(query_c, [clean_text(q) for q in questions], n=1, cutoff=0.5)
    if matches:
        idx = [clean_text(q) for q in questions].index(matches[0])
        return FAQ_DATA[questions[idx]]

    return "Sorry, I couldn't find an answer. Please contact NuGenomics support."

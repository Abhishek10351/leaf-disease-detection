"""
Knowledge base seed data for diseases, treatments, and care guides.
This data is indexed into Chroma for RAG.
"""

KNOWLEDGE_BASE_SEED = {
    "diseases": [
        {
            "id": "powdery_mildew",
            "name": "Powdery Mildew",
            "plant": "rose",
            "severity": "moderate",
            "symptoms": "white powdery coating on leaves, leaf curling, stunted growth",
            "description": "Powdery mildew is a common fungal disease affecting roses, characterized by white powder-like coating on leaves, stems, and buds. Affected leaves curl upward and may eventually drop. The disease thrives in warm, dry conditions with poor air circulation. Severity ranges from mild (cosmetic damage) to severe (plant death)."
        },
        {
            "id": "early_blight",
            "name": "Early Blight",
            "plant": "tomato",
            "severity": "moderate",
            "symptoms": "brown spots with concentric rings, lower leaves yellow and drop, progressive upward movement",
            "description": "Early blight is a fungal disease primarily affecting tomatoes and potatoes. It appears as brown circular spots with concentric rings (target-like pattern) on lower leaves first. The disease progresses upward as infected leaves yellow and drop. Caused by Alternaria solani, it thrives in warm, wet conditions."
        },
        {
            "id": "leaf_spot",
            "name": "Leaf Spot",
            "plant": "general",
            "severity": "mild",
            "symptoms": "circular or irregular dark spots on leaves, yellow halos, leaf yellowing",
            "description": "Leaf spot diseases are caused by various fungi or bacteria, affecting many plant species. Symptoms include circular to irregular dark spots on leaf surfaces, often surrounded by yellow halos. Spots may coalesce, causing entire leaves to yellow and drop. The disease is spread by water splash and thrives in humid conditions."
        },
        {
            "id": "rust",
            "name": "Rust",
            "plant": "general",
            "severity": "moderate",
            "symptoms": "orange, reddish-brown powdery pustules on leaf undersides, yellowing of upper leaf surface",
            "description": "Rust diseases are caused by fungal pathogens that produce distinctive orange to reddish-brown pustules (spore-producing structures) on leaf undersides. Upper leaf surface typically yellows. Rust thrives in wet, humid conditions. Different rust species affect different hosts. Can significantly reduce plant vigor if untreated."
        },
        {
            "id": "mosaicvirus",
            "name": "Mosaic Virus",
            "plant": "general",
            "severity": "severe",
            "symptoms": "mottled yellowing of leaves, leaf distortion and curling, stunted growth, reduced yield",
            "description": "Mosaic viruses cause mottled, variegated coloring on leaves, with yellowing and distortion. Symptoms include leaf curling, stunting, and severe reduction in plant vigor and productivity. Aphids and whiteflies commonly transmit mosaic viruses. No cure exists; prevention through resistant varieties is best strategy. Can devastate crops if not controlled."
        }
    ],
    "treatments": [
        {
            "id": "treat_pm_sulfur",
            "disease": "powdery_mildew",
            "method": "sulfur spray",
            "description": "Apply elemental sulfur spray at 2-3 week intervals during growing season. Mix 2-3 tablespoons of sulfur per gallon of water. Spray thoroughly, covering both leaf surfaces. Apply in early morning or late evening to avoid leaf burn. Sulfur is effective and organic-approved. Not suitable for use within 2 weeks of oil applications.",
            "effectiveness": "high",
            "organic": True,
            "application_rate": "2-3 tbsp per gallon",
            "frequency": "every 2-3 weeks"
        },
        {
            "id": "treat_pm_neem",
            "disease": "powdery_mildew",
            "method": "neem oil",
            "description": "Neem oil is an organic fungicide effective against powdery mildew and many other diseases. Dilute neem oil according to label directions (typically 2-3% solution). Spray thoroughly covering all leaf surfaces. Apply in early morning or evening to avoid leaf damage. Reapply every 7-14 days as needed.",
            "effectiveness": "medium",
            "organic": True,
            "application_rate": "2-3% solution",
            "frequency": "every 7-14 days"
        },
        {
            "id": "treat_eb_copper",
            "disease": "early_blight",
            "method": "copper fungicide",
            "description": "Copper sulfate fungicides are effective against early blight on tomatoes. Apply at first sign of disease symptoms. Mix 2-3 tablespoons copper fungicide per gallon of water. Spray thoroughly, covering all leaf surfaces. Reapply every 7-10 days throughout growing season, or after heavy rain.",
            "effectiveness": "high",
            "organic": True,
            "application_rate": "2-3 tbsp per gallon",
            "frequency": "every 7-10 days"
        },
        {
            "id": "treat_eb_chlorothalonil",
            "disease": "early_blight",
            "method": "chlorothalonil",
            "description": "Chemical fungicide effective against early blight. Follow label instructions carefully. Apply preventively or at first sign of symptoms. Reapply every 7 days or after rain. Not organic-approved but highly effective. Use with proper safety equipment.",
            "effectiveness": "very high",
            "organic": False,
            "application_rate": "per label",
            "frequency": "every 7 days"
        },
        {
            "id": "treat_general_removal",
            "disease": "general",
            "method": "infected leaf removal",
            "description": "Remove infected leaves as soon as disease is noticed. For fungal diseases, this can slow spread significantly. Remove entire affected leaf and dispose in trash (not compost). Sterilize pruning tools between cuts with 10% bleach solution to prevent spread. This organic method works best combined with other treatments.",
            "effectiveness": "medium",
            "organic": True,
            "application_rate": "as needed",
            "frequency": "ongoing"
        }
    ],
    "care_guides": [
        {
            "id": "care_rose",
            "plant": "rose",
            "difficulty": "moderate",
            "season": "spring-fall",
            "description": "Roses require full sun (6+ hours daily), well-drained soil rich in organic matter, and regular watering (1-2 inches weekly). Prune in early spring to 12-18 inches. Deadhead spent flowers to encourage blooming. Fertilize every 4-6 weeks during growing season. Space plants 3 feet apart for air circulation to prevent diseases. Mulch with 2-3 inches of organic material."
        },
        {
            "id": "care_tomato",
            "plant": "tomato",
            "difficulty": "easy",
            "season": "spring-summer",
            "description": "Tomatoes need full sun, warm temperatures (70-85°F), and consistently moist soil. Water deeply at base, avoiding foliage to prevent disease. Use cages or stakes for support. Fertilize every 2-3 weeks with balanced fertilizer. Prune suckers (growth between main stem and branches) for better air circulation. Space plants 24-36 inches apart. Harvest when fully colored for best flavor."
        },
        {
            "id": "care_general_watering",
            "plant": "general",
            "difficulty": "easy",
            "season": "year-round",
            "description": "Most plants need 1-2 inches of water per week, including rainfall. Water deeply and less frequently rather than shallow daily watering to encourage deep root growth. Water at base of plants in early morning to minimize disease. Avoid wetting foliage. Check soil moisture before watering (soil should be moist to 2-3 inches deep, not soggy). Adjust frequency for your climate."
        },
        {
            "id": "care_general_soil",
            "plant": "general",
            "difficulty": "easy",
            "season": "year-round",
            "description": "Quality soil is foundation of plant health. Use well-draining potting mix or garden soil amended with compost. Soil pH should be 6.0-7.0 for most plants. Add 2-3 inches of mulch around plants (keeping away from stem) to maintain moisture and temperature. Refresh mulch annually. For container plants, repot every 1-2 years with fresh soil."
        }
    ]
}

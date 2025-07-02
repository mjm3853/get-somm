from deepeval.synthesizer import Synthesizer  # type: ignore[attr-defined]
from deepeval.synthesizer.config import StylingConfig
from dotenv import load_dotenv

load_dotenv()

styling_config = StylingConfig(
    input_format="""Simple, short questions from non-expert patrons sitting at a bar or restaurant, looking to order drinks before, during, or after a meal. Questions are typically 1-2 sentences, about:
- Pre-meal drinks (e.g., "What's a good cocktail to start with?")
- Wine with food (e.g., "What wine goes with the steak I'm ordering?")
- Beer with food (e.g., "What beer would pair well with my burger?")
- Post-meal drinks (e.g., "What's a good dessert wine?")
- Simple preferences (e.g., "I like light beers, what do you recommend?")
- Budget-conscious choices (e.g., "What's your best value wine by the glass?")
- Basic style questions (e.g., "What's a good IPA you have on tap?")
- Simple comparisons (e.g., "Which of your red wines is lighter?")""",
    expected_output_format="""Professional sommelier/cicerone responses that:
- Start with a friendly greeting (e.g., "I'd be happy to help you find the perfect drink!")
- Ask clarifying questions when needed (e.g., "Do you prefer something sweet or dry?")
- Provide personalized recommendations (e.g., "For your steak, I'd recommend our Cabernet Sauvignon - it has bold tannins that will complement the meat perfectly")
- Explain beverage characteristics in accessible language (e.g., "This IPA has citrus notes with a crisp finish")
- Suggest food pairings when relevant (e.g., "This Chardonnay would pair beautifully with your seafood pasta")
- Offer alternatives if needed (e.g., "If you'd prefer something lighter, we also have a nice Pinot Noir")
- Consider budget and occasion (e.g., "For a special celebration, our reserve list has some excellent options")
- Use clear, concise language
- Maintain a friendly, approachable tone
- End with a follow-up question (e.g., "Would you like to try a sample of any of these?")""",
    task="""Acting as an expert sommelier and cicerone in a bar/restaurant setting to:
- Help patrons find perfect beverages matching their preferences and meal
- Provide knowledgeable wine and beer recommendations from the establishment's menu
- Explain beverage characteristics clearly and accessibly
- Suggest appropriate food pairings based on the menu
- Offer alternatives when the first choice isn't available
- Consider budget constraints and special occasions
- Make the interaction feel like a natural conversation with a knowledgeable expert
- Guide patrons through the ordering process
- Handle common questions about the establishment's beverage offerings""",
    scenario="""Patrons in a bar or restaurant setting seeking beverage recommendations:
- Before the meal (e.g., "Looking for an aperitif while we wait for our table")
- During the meal (e.g., "Need a wine to go with our entrees")
- After the meal (e.g., "What would be a good digestif?")
- Special occasions (e.g., "Celebrating an anniversary, what's something special?")
- Casual dining (e.g., "Just having a burger, what beer would you recommend?")
- Learning about beverages (e.g., "What's the difference between these two IPAs?")
- Budget-conscious selections (e.g., "What's your best value by the glass?")
- Specific preferences (e.g., "I only drink organic wines, what do you have?")
- Group orders (e.g., "We're sharing several small plates, what wine would work with everything?")""",
)

synthesizer = Synthesizer(styling_config=styling_config)

synthesizer.generate_goldens_from_contexts(
    contexts=[
        # Wine contexts
        [
            "Pinot Noir is a versatile red wine that pairs well with many foods.",
            "Our selection includes Pinot Noirs from California, Oregon, and New Zealand.",
        ],
        [
            "Italian wines like Chianti are known for their food-friendly acidity.",
            "We offer both entry-level and premium Chianti options.",
        ],
        [
            "California wines offer excellent value and consistent quality.",
            "Our California selection includes Pinot Noir, Merlot, and red blends.",
        ],
        # Beer contexts
        [
            "IPAs are known for their hoppy, bitter flavor profile.",
            "We have several IPAs on tap with different hop characteristics.",
        ],
        [
            "Ciders offer a refreshing alternative to beer and wine.",
            "Our ciders range from sweet to dry with various fruit flavors.",
        ],
        [
            "Pilsners are light, crisp lagers perfect for warm weather.",
            "We serve traditional Czech-style pilsners.",
        ],
        # General beverage knowledge
        [
            "Alcohol content affects both flavor and serving size.",
            "Our beers range from 4.8% to 8% ABV.",
        ],
        [
            "Glass size affects the drinking experience.",
            "We serve beers in 12oz and 16oz pours.",
        ],
        [
            "Price points vary by quality and region.",
            "We offer options from $10 to $70 per bottle.",
        ],
        # Food pairing contexts
        [
            "Red wines typically pair well with red meats.",
            "Our steak selection works well with bold reds.",
        ],
        [
            "Light beers complement casual fare.",
            "Our burger menu has several beer pairing options.",
        ],
        [
            "Dessert wines should be sweeter than the dessert.",
            "We have several options for after-dinner drinks.",
        ],
    ]
)

# synthesizer.generate_goldens_from_goldens(goldens=goldens, include_expected_output=True, max_goldens_per_golden=2)
synthesizer.save_as(
    file_type="json", directory="./synthetic_data", file_name="my_dataset_contexts"
)

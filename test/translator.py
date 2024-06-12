from googletrans import Translator
import googletrans

translator = Translator()

formatted_text = {
    "introduction": "Goa, located on the west coast of India, is India's smallest state, known for its beautiful beaches, vibrant nightlife, delicious seafood and Portuguese heritage. Well-known for its tolerant and welcoming lifestyle, it offers a unique blend of Indian and Portuguese cultures.",
    "itinerary": [
        {
            "Day": "1",
            "afternoon": "Enjoy a delightful lunch at the Gunpowder restaurant. Post lunch, visit the Archaeological Museum of Goa, and then make your way to Dona Paula viewpoint via commute.",
            "evening": "Have tea and snacks at Cafe Bodega and proceed to visit the Goa Science Centre & Planetarium. Party at Tito's Club in the evening.",
            "morning": "Start your day with breakfast at Artjuna Garden Cafe. Then, visit the famous Fort Aguada, and take a commute to explore the Basilica of Bom Jesus, a UNESCO World Heritage Site.",
            "night": "Dine at Suzie The Bombay Cooking Studio & Dining and stroll along Miramar Beach. Overnight at your stay."
        },
        {
            "Day": "2",
            "afternoon": "Lunch at Suzie The Bombay Cooking Studio & Dining. Post lunch, visit the Museum of Goa, and then commute to the Goa State Museum.",
            "evening": "Enjoy an evening snack at Pousada By The Beach and proceed to visit the Dr. Salim Ali Bird Sanctuary. Later, groove to the music at the Cabana Club.",
            "morning": "Start with breakfast at Eva Cafe. Visit the Salim Ali Bird Sanctuary and take a river cruise on the Mandovi river.",
            "night": "Dine at S.E.A- STRAND OF EXOTIC ASIA and take a peaceful walk on Calangute Beach. Return to your stay for the night."
        },
        {
            "Day": "3",
            "afternoon": "Enjoy lunch at the Fisherman's Wharf. Visit the Church of St. Cajetan and then ride to the Bondla Wildlife Sanctuary.",
            "evening": "Grab snacks at the Navtara Veg Restaurant. Spend your evening at the Baga Beach and enjoy the nightlife at Cafe Mambos.",
            "morning": "Have breakfast at the Infantaria Cafe. Explore the Calangute Market and enjoy water sports at Calangute Beach.",
            "night": "Enjoy a lovely dinner at Vinayak Family Restaurant and visit the night market at Anjuna. Overnight at your stay."
        }
    ]
}

print(formatted_text["itinerary"][1]["afternoon"])

for i in range(0, len(formatted_text["itinerary"])):
    formatted_text["itinerary"][i]["Day"] = translator.translate(formatted_text["itinerary"][i]["Day"], src='en', dest='bn').text
    formatted_text["itinerary"][i]["afternoon"] = translator.translate(formatted_text["itinerary"][i]["afternoon"], src='en', dest='bn').text
    formatted_text["itinerary"][i]["evening"] = translator.translate(formatted_text["itinerary"][i]["evening"], src='en', dest='bn').text
    formatted_text["itinerary"][i]["morning"] = translator.translate(formatted_text["itinerary"][i]["morning"], src='en', dest='bn').text
    formatted_text["itinerary"][i]["night"] = translator.translate(formatted_text["itinerary"][i]["night"], src='en', dest='bn').text

    print(formatted_text["itinerary"][i]["Day"])
    print(formatted_text["itinerary"][i]["afternoon"])
    print(formatted_text["itinerary"][i]["evening"])
    print(formatted_text["itinerary"][i]["morning"])
    print(formatted_text["itinerary"][i]["night"])

print(formatted_text)
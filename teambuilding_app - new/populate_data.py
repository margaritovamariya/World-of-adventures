from extensions import db
from models import Department, Category, Product
from app import app

def populate_data():
    with app.app_context():
        # Изчистване на базата преди зареждане (по избор)
        db.drop_all()
        db.create_all()

        # Данни за добавяне
        data = {
            "Team Adventures": {
                "Outdoor": [
                    {"name": "Hiking Adventure", "description": "Guided mountain hike", "price": 50},
                    {"name": "Rock Climbing Challenge", "description": "Professional climbing experience", "price": 80},
                    {"name": "River Rafting", "description": "Thrilling river descent", "price": 100},
                    {"name": "Forest Escape", "description": "Nature-based team-building activities", "price": 60},
                    {"name": "Camping Under the Stars", "description": "Overnight camping trip", "price": 70},
                    {"name": "Beach Games", "description": "Beach volleyball and team games", "price": 40},
                    {"name": "Orienteering Race", "description": "Map-based adventure in the wild", "price": 50},
                    {"name": "Kayaking Expedition", "description": "Calm lake or river kayaking", "price": 90},
                    {"name": "Wildlife Safari", "description": "Explore local wildlife", "price": 120},
                    {"name": "Zipline Adventure", "description": "High-speed ziplining through trees", "price": 75},
                ],
                "Indoor": [
                    {"name": "Indoor Rock Climbing", "description": "Safe climbing environment", "price": 45},
                    {"name": "Escape Room Challenge", "description": "Team puzzle-solving experience", "price": 30},
                    {"name": "Bowling Tournament", "description": "Friendly competition at a bowling alley", "price": 25},
                    {"name": "Laser Tag Arena", "description": "Action-packed fun for groups", "price": 40},
                    {"name": "Trampoline Park", "description": "High-energy jumping activities", "price": 35},
                    {"name": "VR Team Adventures", "description": "Virtual reality challenges", "price": 60},
                    {"name": "Indoor Archery", "description": "Learn archery skills indoors", "price": 50},
                    {"name": "Pool and Billiards Night", "description": "Relaxed competition", "price": 20},
                    {"name": "Karaoke Battle", "description": "Team singing competition", "price": 30},
                    {"name": "Indoor Mini-Golf", "description": "Fun and challenging courses", "price": 25},
                ],
                "Adrenaline": [
                    {"name": "Skydiving Tandem Jump", "description": "High-thrill freefall", "price": 250},
                    {"name": "Bungee Jump", "description": "Leap from a high bridge", "price": 200},
                    {"name": "Off-Road ATV Adventure", "description": "Explore rugged terrain", "price": 150},
                    {"name": "Paragliding Flight", "description": "Scenic aerial adventure", "price": 180},
                    {"name": "Paintball Battle", "description": "Strategic outdoor shooting game", "price": 50},
                    {"name": "High Rope Course", "description": "Rope bridges and ziplines", "price": 70},
                    {"name": "Whitewater Kayaking", "description": "Navigate rapids with your team", "price": 120},
                    {"name": "Free Climbing", "description": "Advanced climbing with instructors", "price": 100},
                    {"name": "Jet Ski Racing", "description": "High-speed water adventure", "price": 80},
                    {"name": "Zorbing Experience", "description": "Roll down a hill in a giant ball", "price": 50},
                ],
            },
            "Unforgettable Celebrations": {
                "Children's Birthday Party": [
                    {"name": "Magic Show", "description": "Interactive magic tricks", "price": 100},
                    {"name": "Face Painting", "description": "Creative designs for kids", "price": 50},
                    {"name": "Balloon Animals Workshop", "description": "Learn balloon twisting", "price": 60},
                    {"name": "Clown Performance", "description": "Entertaining comedy show", "price": 90},
                    {"name": "Puppet Show", "description": "Storytelling with puppets", "price": 70},
                    {"name": "DIY Craft Corner", "description": "Arts and crafts activities", "price": 50},
                    {"name": "Mini Disco", "description": "Kid-friendly dance party", "price": 80},
                    {"name": "Treasure Hunt", "description": "Interactive adventure for kids", "price": 40},
                    {"name": "Inflatable Castle", "description": "Bounce house rental", "price": 100},
                    {"name": "Science Experiments", "description": "Fun educational show", "price": 120},
                ],
                "Bachelorette Party": [
                    {"name": "Spa Day", "description": "Relaxation and pampering", "price": 150},
                    {"name": "Wine Tasting Tour", "description": "Private vineyard experience", "price": 200},
                    {"name": "Dance Class", "description": "Fun lessons in salsa or other styles", "price": 100},
                    {"name": "Personalized Cocktails", "description": "Custom drinks for the group", "price": 120},
                    {"name": "Luxury Dinner", "description": "Fine dining experience", "price": 250},
                    {"name": "Comedy Club Night", "description": "Laughter-filled evening", "price": 60},
                    {"name": "Private Karaoke Room", "description": "Sing the night away", "price": 80},
                    {"name": "Makeup Workshop", "description": "Professional makeup tutorial", "price": 70},
                    {"name": "Private Yoga Class", "description": "Relaxation and mindfulness", "price": 90},
                    {"name": "Limo Party Tour", "description": "Night out in style", "price": 300},
                ],
                "Company Party": [
                    {"name": "Gala Dinner", "description": "Elegant setup with catering.", "price": 300},
                    {"name": "Live Music Band", "description": "Performances for all tastes.", "price": 500},
                    {"name": "Themed Costume Party", "description": "Dress up and compete.", "price": 250},
                    {"name": "Trivia Night", "description": "Fun questions for everyone.", "price": 100},
                    {"name": "Casino Night", "description": "Roulette and poker tables.", "price": 200},
                    {"name": "Outdoor BBQ Party", "description": "Relaxed company outing.", "price": 150},
                    {"name": "Game Night", "description": "Board and video games.", "price": 120},
                    {"name": "Award Ceremony", "description": "Celebrate team achievements.", "price": 100},
                    {"name": "DJ Night", "description": "Professional DJ for dancing.", "price": 400},
                    {"name": "Photo Booth Rental", "description": "Capture the memories.", "price": 80},
                ],
                "Bachelor Party": [
                    {"name": "Craft Beer Tasting", "description": "Local brewery tour.", "price": 150},
                    {"name": "Poker Night", "description": "Professional poker setup.", "price": 100},
                    {"name": "Axe Throwing", "description": "Test your skills with friends.", "price": 80},
                    {"name": "Whiskey Tasting", "description": "Sampling premium whiskeys.", "price": 200},
                    {"name": "Go-Kart Racing", "description": "High-speed action.", "price": 120},
                    {"name": "Shooting Range Experience", "description": "Target shooting fun.", "price": 100},
                    {"name": "Nightclub VIP Access", "description": "Skip the lines.", "price": 250},
                    {"name": "Sports Game Night", "description": "Watch live sports as a group.", "price": 180},
                    {"name": "Escape Room for Men", "description": "Themed puzzles for guys.", "price": 70},
                    {"name": "Road Trip Adventure", "description": "Custom-planned trip.", "price": 400},
                ],
            },
            "Private Events": {
                "Family Gatherings": [
                    {"name": "Backyard BBQ", "description": "Relaxed barbecue gathering with family.", "price": 150},
                    {"name": "Picnic in the Park", "description": "Organized family picnic with activities.", "price": 100},
                    {"name": "Game Night", "description": "Board and card games for the whole family.", "price": 50},
                    {"name": "Movie Under the Stars", "description": "Outdoor cinema setup for families.", "price": 200},
                    {"name": "Potluck Dinner", "description": "Coordinated family-style dinner event.", "price": 120},
                    {"name": "Kids Play Area", "description": "Dedicated space for kids to have fun.", "price": 80},
                    {"name": "Family Trivia Night", "description": "Interactive trivia for family teams.", "price": 70},
                    {"name": "Storytelling Session", "description": "Professional storyteller for children and adults.", "price": 90},
                    {"name": "Cultural Evening", "description": "Family event with cultural performances.", "price": 180},
                    {"name": "Family Portrait Session", "description": "Professional photographer for family pictures.", "price": 150},
                ],
                "Anniversary Celebration": [
                    {"name": "Romantic Dinner", "description": "Candlelit dinner for two.", "price": 200},
                    {"name": "Live Music Performance", "description": "Acoustic artist for private events.", "price": 300},
                    {"name": "Couples Dance Class", "description": "Learn new dance moves together.", "price": 150},
                    {"name": "Anniversary Cake", "description": "Custom cake for the occasion.", "price": 100},
                    {"name": "Photo Slideshow Setup", "description": "Showcase your memories on a big screen.", "price": 120},
                    {"name": "Private Venue Rental", "description": "Exclusive use of a venue.", "price": 500},
                    {"name": "Decor Package", "description": "Elegant anniversary decorations.", "price": 250},
                    {"name": "Vow Renewal Ceremony", "description": "Celebrate your love with renewed vows.", "price": 400},
                    {"name": "Wine Pairing Dinner", "description": "Dinner with selected wine pairings.", "price": 300},
                    {"name": "Sky Lantern Release", "description": "Symbolic lantern release for the couple.", "price": 180},
                ],
                "Romantic Dinner": [
                    {"name": "Beachside Dinner", "description": "Dine by the waves under the stars.", "price": 300},
                    {"name": "Private Chef Experience", "description": "Chef-prepared meal in your home.", "price": 350},
                    {"name": "Wine and Dine", "description": "Three-course meal with wine.", "price": 250},
                    {"name": "Rooftop Dinner", "description": "Elegant dinner with a view.", "price": 280},
                    {"name": "Themed Dinner Night", "description": "Special dinner with a unique theme.", "price": 220},
                    {"name": "Couple's Dessert Tasting", "description": "Selection of fine desserts.", "price": 150},
                    {"name": "Flower Arrangement Setup", "description": "Romantic floral decorations.", "price": 100},
                    {"name": "Candlelit Garden Dinner", "description": "Dinner surrounded by greenery.", "price": 200},
                    {"name": "Picnic Basket Dinner", "description": "Pre-packed gourmet dinner for two.", "price": 120},
                    {"name": "Live Violinist", "description": "Music accompaniment for your dinner.", "price": 200},
                ],
                "Private Tour": [
                    {"name": "Historical City Walk", "description": "Private guide to explore city history.", "price": 180},
                    {"name": "Winery Tour", "description": "Private visit to a local vineyard.", "price": 250},
                    {"name": "Museum Exclusive Access", "description": "After-hours tour of the museum.", "price": 300},
                    {"name": "Nature Hiking Tour", "description": "Guided hike with a focus on nature.", "price": 150},
                    {"name": "Art Gallery Tour", "description": "Personalized tour of local art galleries.", "price": 200},
                    {"name": "Boat Tour", "description": "Private boat ride with guide.", "price": 400},
                    {"name": "Helicopter Tour", "description": "Aerial tour of key attractions.", "price": 800},
                    {"name": "Food Tasting Tour", "description": "Taste the best of local cuisine.", "price": 180},
                    {"name": "Street Art Tour", "description": "Discover hidden art in the city.", "price": 120},
                    {"name": "Photography Tour", "description": "Private guide to capture scenic locations.", "price": 220},
                ],
            },
            "Corporate Events": {
                "Conferences": [
                    {"name": "Keynote Speaker", "description": "Engaging presentation by an industry expert.", "price": 1000},
                    {"name": "Conference Room Rental", "description": "Fully equipped room for corporate meetings.", "price": 500},
                    {"name": "AV Equipment Setup", "description": "Audio-visual support for your event.", "price": 300},
                    {"name": "On-Site Catering", "description": "Food and beverages for conference attendees.", "price": 700},
                    {"name": "Registration Desk Management", "description": "Staffed desk for attendee check-ins.", "price": 200},
                    {"name": "Event Branding", "description": "Custom banners, posters, and marketing materials.", "price": 400},
                    {"name": "Networking Session", "description": "Organized activities for business networking.", "price": 350},
                    {"name": "Live Streaming", "description": "Broadcast your event to remote participants.", "price": 800},
                    {"name": "Panel Discussion Moderation", "description": "Experienced moderator for panel discussions.", "price": 500},
                    {"name": "Post-Event Report", "description": "Detailed analysis and feedback from attendees.", "price": 300},
                ],
                "Workshops": [
                    {"name": "Leadership Training", "description": "Interactive training for team leaders.", "price": 600},
                    {"name": "Project Management Workshop", "description": "Essential skills for managing projects.", "price": 500},
                    {"name": "Creative Problem Solving", "description": "Learn innovative ways to address challenges.", "price": 450},
                    {"name": "Effective Communication", "description": "Improve team collaboration and communication.", "price": 400},
                    {"name": "Time Management Skills", "description": "Techniques to manage time effectively.", "price": 350},
                    {"name": "Customer Service Excellence", "description": "Training on delivering top-notch service.", "price": 400},
                    {"name": "Sales Strategy Workshop", "description": "Build effective sales techniques.", "price": 500},
                    {"name": "Negotiation Skills Training", "description": "Master the art of negotiation.", "price": 450},
                    {"name": "Conflict Resolution", "description": "Practical methods to resolve workplace conflicts.", "price": 400},
                    {"name": "Employee Well-Being", "description": "Workshops to enhance employee wellness.", "price": 300},
                ],
                "Team-Building Retreats": [
                    {"name": "Outdoor Adventure", "description": "Team bonding activities in nature.", "price": 700},
                    {"name": "Problem-Solving Challenges", "description": "Collaborative problem-solving tasks.", "price": 600},
                    {"name": "Cooking Class Retreat", "description": "Team-building through cooking together.", "price": 500},
                    {"name": "Escape Room Adventure", "description": "Team strategy and communication game.", "price": 450},
                    {"name": "Trust-Building Exercises", "description": "Activities to build trust among team members.", "price": 400},
                    {"name": "Leadership Development", "description": "Develop leadership skills in a retreat setting.", "price": 800},
                    {"name": "Outdoor Sports Competitions", "description": "Friendly team competitions.", "price": 400},
                    {"name": "Creative Workshops", "description": "Art, writing, or other creative group activities.", "price": 350},
                    {"name": "Relaxation Retreat", "description": "Focus on wellness and stress relief.", "price": 600},
                    {"name": "Innovation Challenge", "description": "Foster creativity with innovative tasks.", "price": 700},
                ],
                "Product Launches": [
                    {"name": "Stage Design", "description": "Eye-catching stage setup for product unveiling.", "price": 1500},
                    {"name": "Event Hosting", "description": "Professional host to guide the event.", "price": 800},
                    {"name": "Product Demo Booth", "description": "Interactive demo area for your product.", "price": 1000},
                    {"name": "Media Coverage", "description": "Press and media coverage for your launch.", "price": 1200},
                    {"name": "Event Invitations", "description": "Custom-designed invitations for your guests.", "price": 300},
                    {"name": "Social Media Marketing", "description": "Promote your event on social platforms.", "price": 700},
                    {"name": "Photography and Videography", "description": "Capture the event with professional visuals.", "price": 1000},
                    {"name": "Product Branding Materials", "description": "Banners, flyers, and branded items.", "price": 500},
                    {"name": "Entertainment", "description": "Music, performances, or other entertainment.", "price": 1200},
                    {"name": "Post-Event Follow-Up", "description": "Email campaigns and feedback collection.", "price": 400},
                ],
            },
        }

        # Добавяне на отдели, категории и продукти
        for department_name, categories in data.items():
            department = Department(name=department_name)
            db.session.add(department)
            db.session.flush()

            for category_name, products in categories.items():
                category = Category(name=category_name, department_id=department.id)
                db.session.add(category)
                db.session.flush()

                for product in products:
                    new_product = Product(
                        name=product["name"],
                        description=product["description"],
                        price=product["price"],
                        category_id=category.id,
                    )
                    db.session.add(new_product)

        # Запазване на промените
        db.session.commit()
        print("Database populated successfully with all data!")

if __name__ == "__main__":
    populate_data()

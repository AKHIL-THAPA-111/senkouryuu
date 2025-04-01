import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import random
import time
import csv
import os
import base64
from Head import *
# 📌 Import Gemini API
def set_dark_mode():
    st.set_page_config(layout="wide")
    st.markdown(
        """
        <style>
            body {
                background-color: #0e1117;
                color: white;
            }
            [data-testid="stAppViewContainer"] {
                background-color: #0e1117;
            }
            [data-testid="stSidebar"] {
                background-color: #161a23;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

set_dark_mode()

dance = "https://cdn.dribbble.com/userupload/20078936/file/original-190053e8da73440a535a4fc3d5b9d77a.gif"

quotes = [
    "🌟 *“Success is not final, failure is not fatal: It is the courage to continue that counts.”* – Winston Churchill",
    "🔥 *“Do not be embarrassed by your failures, learn from them and start again.”* – Richard Branson",
    "💡 *“The only way to do great work is to love what you do.”* – Steve Jobs",
    "🚀 *“Believe you can and you're halfway there.”* – Theodore Roosevelt",
    "⏳ *“Success usually comes to those who are too busy to be looking for it.”* – Henry David Thoreau",
    "⚙️ *“Opportunities don't happen. You create them.”* – Chris Grosser",
    "💬 *“Don't be pushed around by the fears in your mind. Be led by the dreams in your heart.”* – Roy T. Bennett",
    "🌍 *“Your time is limited, so don’t waste it living someone else’s life.”* – Steve Jobs",
    "📚 *“Do one thing every day that scares you.”* – Eleanor Roosevelt",
    "⚡ *“What you get by achieving your goals is not as important as what you become by achieving your goals.”* – Zig Ziglar",
    "🌈 *“The only limit to our realization of tomorrow is our doubts of today.”* – Franklin D. Roosevelt",
    "🌿 *“Happiness is not something ready-made. It comes from your own actions.”* – Dalai Lama",
    "💡 *“Everything you’ve ever wanted is on the other side of fear.”* – George Addair",
    "🔥 *“Hardships often prepare ordinary people for an extraordinary destiny.”* – C.S. Lewis",
    "⚙️ *“Success is walking from failure to failure with no loss of enthusiasm.”* – Winston Churchill",
    "🎯 *“The road to success and the road to failure are almost exactly the same.”* – Colin R. Davis",
    "🌅 *“Don’t watch the clock; do what it does. Keep going.”* – Sam Levenson",
    "🌠 *“Keep your face always toward the sunshine—and shadows will fall behind you.”* – Walt Whitman",
    "🎓 *“Do not wait to strike till the iron is hot, but make it hot by striking.”* – William Butler Yeats",
    "🧠 *“Your limitation—it’s only your imagination.”* – Unknown",
    "💥 *“Push yourself, because no one else is going to do it for you.”* – Unknown",
    "🔥 *“Great things never come from comfort zones.”* – Unknown",
    "🌌 *“Dream it. Wish it. Do it.”* – Unknown",
    "🎯 *“Success doesn’t just find you. You have to go out and get it.”* – Unknown",
    "⚡ *“The harder you work for something, the greater you’ll feel when you achieve it.”* – Unknown",
    "🏅 *“Dream bigger. Do bigger.”* – Unknown",
    "🌟 *“Don’t stop when you’re tired. Stop when you’re done.”* – Unknown",
    "🔑 *“Wake up with determination. Go to bed with satisfaction.”* – Unknown",
    "🔥 *“Do something today that your future self will thank you for.”* – Unknown",
    "💡 *“Little things make big days.”* – Unknown",
    "🚀 *“It’s going to be hard, but hard does not mean impossible.”* – Unknown",
    "⚙️ *“Don’t wait for opportunity. Create it.”* – Unknown",
    "🌍 *“Sometimes we’re tested not to show our weaknesses, but to discover our strengths.”* – Unknown",
    "🌈 *“The key to success is to focus on goals, not obstacles.”* – Unknown",
    "🎯 *“Dream it. Believe it. Build it.”* – Unknown",
    "🔥 *“Success is not in what you have, but who you are.”* – Bo Bennett",
    "💡 *“Your big opportunity may be right where you are now.”* – Napoleon Hill",
    "⚙️ *“In the middle of every difficulty lies opportunity.”* – Albert Einstein",
    "🌠 *“Don’t count the days, make the days count.”* – Muhammad Ali",
    "🔑 *“Success is getting what you want. Happiness is wanting what you get.”* – Dale Carnegie",
    "🌅 *“Courage is one step ahead of fear.”* – Coleman Young",
    "🎓 *“You miss 100% of the shots you don’t take.”* – Wayne Gretzky",
    "🚀 *“Failure is not the opposite of success; it’s part of success.”* – Arianna Huffington",
    "🔥 *“It always seems impossible until it’s done.”* – Nelson Mandela",
    "⚡ *“Start where you are. Use what you have. Do what you can.”* – Arthur Ashe",
    "🌍 *“The future belongs to those who believe in the beauty of their dreams.”* – Eleanor Roosevelt",
    "💬 *“Do what you can, with what you have, where you are.”* – Theodore Roosevelt",
    "🌿 *“Everything you can imagine is real.”* – Pablo Picasso",
    "🌈 *“Act as if what you do makes a difference. It does.”* – William James",
    "🚀 *“Don’t be afraid to give up the good to go for the great.”* – John D. Rockefeller"

]
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            min-width: 300px;
            max-width: 600px;
            resize: horizontal;  /* 
            overflow: auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)






# Use the GitHub raw URL
image_url = "https://raw.githubusercontent.com/AKHIL-THAPA-111/senkouryuu/main/ok.jpg"

# Apply background image
background_image = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("{image_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)



# Sidebar content



# 🔥 Amazon Query Conversion Function


# 🔑 ScraperAPI Configuration

BASE_URL = "https://www.amazon.in"

NUM_PAGES = 5
CLEANED_CSV = "cleaned_amazon_products.csv"
RETRY_LIMIT = 5
TIMEOUT = 15  
USER_AGENTS = Headers.head()


# ✅ Initialize session variables safely

if "status" not in st.session_state:
    st.session_state.status = ""
if "data" not in st.session_state:
    st.session_state.data = None


# 🌟 Function to Fetch HTML with ScraperAPI
def fetch(url, retries=RETRY_LIMIT):
    """Fetch a URL using ScraperAPI with retries and timeouts"""
    headers = USER_AGENTS

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=TIMEOUT,verify=False)
            
            if response.status_code == 200:
                return response.text
            elif response.status_code in [403, 503]:
                print(f"⚠️ Blocked: {url}. Retrying... ({attempt + 1}/{retries})")
        except requests.RequestException as e:
            print(f"⚠️ Error fetching {url}: {e}")

        time.sleep(random.uniform(1, 3))


# ✅ Extract product details from soup
def extract_product_details(soup, product_url):
    """Extract product details safely"""
    def get_text(selector):
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else "N/A"

    return {
        "Title": get_text("#productTitle"),
        "Price": get_text(".a-price-whole"),
        "Rating": get_text(".a-icon-alt"),
        "Reviews": get_text("#acrCustomerReviewText"),
        "Availability": get_text("#availability span"),
        "URL": product_url  
        
    }


# ✅ Fetch product details safely with progress update
# ✅ Fetch product details safely with progress update
def fetch_product_details(product_url, idx, data_list, total, image_url="N/A"):
    """Fetch product details and update progress safely"""
    html = fetch(product_url)

    if html:
        soup = BeautifulSoup(html, "lxml")
        details = extract_product_details(soup, product_url)
        
        # Add image URL, even if it's missing
        details["Image_URL"] = image_url if image_url != "N/A" else "https://via.placeholder.com/150"

        data_list.append(details)
        print(f"✅ Product {idx + 1}/{total}: {details['Title']}")


# ✅ Get product links from search results
def get_product_links(search_query, page_num):
    """Fetch product links and image URLs together"""
    search_url = f"{BASE_URL}/s?k={search_query}&page={page_num}"
    html = fetch(search_url)
    
    if html:
        soup = BeautifulSoup(html, "lxml")
        
        products = []
        
        # Extract product containers
        containers = soup.select("div.s-main-slot div.s-result-item")
        
        for container in containers:
            # Extract product link
            link_element = container.select_one("a.a-link-normal.s-no-outline")
            if link_element and "/dp/" in link_element.get("href", ""):
                link = BASE_URL + link_element["href"].split("?")[0]

                # Extract image URL from the same container
                img_element = container.select_one("img.s-image")
                img_url = img_element["src"] if img_element else "N/A"
                

                products.append({"link": link, "image": img_url})

        return products

    return []



# ✅ Main Scraping Logic with Caching
@st.cache_data(ttl=3600)
def scrape_data(search_query, num_pages,_progress_bar):
    """Main function to scrape and cache data"""
    all_product_links = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda page: get_product_links(search_query, page), range(1, num_pages + 1)))

    # Flatten and extract product links and images
    all_product_links = [
        {"link": item["link"], "image": item["image"]}
        for sublist in results if sublist for item in sublist
    ]
    
    st.success(f"✅ Found {len(all_product_links)} unique products!")

    product_data = []
    total_products = len(all_product_links)

    # Progress and status


    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
     futures = [
        executor.submit(
            fetch_product_details, 
            product["link"], idx, product_data, total_products, product["image"]
        )
        for idx, product in enumerate(all_product_links)
    ]
    
    # Progress tracking
     completed = 0
     for future in concurrent.futures.as_completed(futures):
        future.result()
        completed += 1
        progress_bar.progress(completed / total_products)
        caption = random.choice(quotes)
        progress_bar.progress(completed / total_products, text=f"{caption} ({completed}/{total_products})")
        


    # Save data with image URLs
    with open(CLEANED_CSV, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Title", "Price", "Rating", "Reviews", "Availability", "URL", "Image_URL"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(product_data)
    st.snow()

    # Convert to DataFrame
    df = pd.DataFrame(product_data)

    # Clean and convert columns
    df['Price'] = pd.to_numeric(df['Price'].str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
    df['Rating'] = pd.to_numeric(df['Rating'].str.extract(r'(\d+\.\d+)')[0], errors='coerce').fillna(0)
    df['Reviews'] = pd.to_numeric(df['Reviews'].str.extract(r'(\d+)')[0], errors='coerce').fillna(0)

    df.to_csv(CLEANED_CSV, index=False)

    st.session_state.data = df

    return df


# ✅ Load previous data from CSV
def load_previous_data():
    """Load the previously saved data from CSV"""
    if os.path.exists(CLEANED_CSV):
        df = pd.read_csv(CLEANED_CSV)
        st.session_state.data = df
        return df
    else:
        st.warning("⚠️ No previous data found.")
        return None


# ✅ Streamlit UI
st.title("*Senkouryuu* :*YOUR AMAZON SCRAPER ⚡*")

# 🎯 User Input Section
# Default empty string if not set before

def get_search_query(query):
    return query.replace(" ", "+")

# Get the Amazon-friendly query format
search_query = get_search_query(st.text_input("**Enter your search query:**", ""))


num_pages = st.slider("**Select number of pages to scrape**", 1, 100, 4)

# 🎯 Scraping or Loading
if st.button("🔎 Scrape Data"):
    img_holder = st.empty()  # Temporary image placeholder
    img_holder.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
      <figure style="text-align: center;">
        <img src="{dance}" alt="Scraping..." width="3000s0" height="300" />
        <figcaption style="margin-bottom: 10px; font-style: italic; color: #fff;">\nScraping in progress...🔃</figcaption>
    </div>
    """,
    unsafe_allow_html=True
)
    progress_bar = st.progress(0)
    with st.spinner("*Scraping in progress...*"):
        df = scrape_data(search_query, num_pages,progress_bar)
        
        # ✅ Use the proper progress update logic inside scrape_data
        if df is not None:
            progress_bar.progress(1.0)  # Set to 100% when complete
            st.session_state.data = df

    img_holder.empty()
    time.sleep(0.5)  # Clears the dancing image
    


if st.button("📂 Load Previous Data"):
    load_previous_data()

# 🎯 Display Filtered Data
# ✅ Display Filtered Data with Images
# ✅ Display Filtered Data with Images
if st.session_state.data is not None:
    df = st.session_state.data

    # Add clickable links with image rendering
    df['Title'] = df.apply(
        lambda row: f"<a href='{row['URL']}' target='_blank'>{row['Title']}</a>", axis=1
    )

    # Render images with a fixed width for consistency
    df['Image'] = df['Image_URL'].apply(
        lambda url: f"<img src='{url}' width='5000000' height='200' />" if pd.notnull(url) else "N/A"
    )

    # Filters
    price_range = st.slider("💰 Price Range", 0, int(df['Price'].max()), (0, int(df['Price'].max())))
    rating_range = st.slider("⭐ Rating Range", 0.0, 5.0, (0.0, 5.0))
    reviews_range = st.slider("📝 Reviews Range", 0, 0, (0, int(df['Reviews'].max()+1)))

    filtered_df = df[
        (df['Price'].between(*price_range)) &
        (df['Rating'].between(*rating_range)) &
        (df['Reviews'].between(*reviews_range))
    ]

    # Display filtered data with images
    st.markdown(
        filtered_df[['Image', 'Title', 'Price', 'Rating', 'Reviews']].to_html(escape=False, index=False), 
        unsafe_allow_html=True
    )

import streamlit as st
import math
import scipy.stats as stats
import random
st.set_page_config(page_title="Luck Analyzer", page_icon="🎰")

st.title("🎰 Gamepull Luck Analyzer")
st.write("Compare your drop rates against the mathematical average.")

# Sidebar Navigation
mode = st.sidebar.radio("Choose Mode:", ["Dry Streak Analysis", "Overall Luck"])

if mode == "Dry Streak Analysis":
    st.header("How unlucky is your streak?")
    packs = st.number_input("What is your current shardless streak?", min_value=1, value=100)
    
    # Calculation
    odds = (1 - pow(0.9975, packs)) * 100
    
    st.metric("Unluckier than", f"{odds:.2f}%")
    st.write(f"In a room of 100 players, **{int(odds)}** would have already found a shard by now.")
    
    if packs >= 1000 and packs < 1200:
        st.error("Welcome to the 1k club 🎉🎉🎉")
    elif packs >=1200 and packs < 2000:
        names=["KingofBasilisk","Mickermouse","Nokister", "maomarc","spegedy","Lua","Pehmo", "Whovianpancake", "EsculantApe", "Dora", "Mike_cee", "Flizor", "ShyPuppet", "lamouuun", "golan", "Frannouche", "Perry3951", "Buzielo", "YellowCake", "Dovah", "RedMan", "Furycad", "Nekoss", "Chreet", "Bushmaster", "Exil", "Gallicien", "Devious", "Tomstoast", "Alf", "HotGayDad", "LeMonke", "Firion", "Ahmphi", "Jörm", "Mickermouse", "Griffin354", "RetroKr1ss", "Sachenfire", "asdfjklsemicolon", "EchoStyx", "sprixis", "Papa Grimace"]
        st.error(f"Have you tried opening one of {names[random.randrange(0,len(names)-1)]}'s sponsored packs")
    elif odds < 50:
        st.error("Still under the mean, keep pulling")
    elif odds > 50 and packs < 1000:
        st.error("Starting to get unlucky, have you tried closing a few tabs?")
    elif packs >= 2000 and packs < 2200:
        st.error("Rare 2k club member")
    elif packs >=220 and packs < 3000:
        st.error("Surely it is coming now")
    elif packs > 3000 and packs < 3400:
        st.error("Only legend himself @Furycad has gone so far, entering unexplored land")
    elif packs > 3400:
        st.error("Record-breaking streak! (Not the kind of record you like to break)")

elif mode == "Overall Luck":
    st.header("Overall Luck Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        all_packs = st.number_input("Total packs opened", min_value=1, value=1000)
        shards = st.number_input("Total shards found", min_value=0, value=2)
    
    with col2:
        ucP = st.number_input("Uncommon packs", value=0)
        rareP = st.number_input("Rare packs", value=0)
        epicP = st.number_input("Epic packs", value=0)
        legP = st.number_input("Legendary packs", value=0)

    if all_packs < 4000:
        st.warning("⚠️ Small sample size. Results may be inconsistent.")

    # Calculations
    basePacks = all_packs - ucP - rareP - epicP - legP
    meanOdds = ((0.0024975 * basePacks) + 
                (0.0037444 * ucP) + 
                (0.00499 * rareP) + 
                (0.0074775 * epicP) + 
                (0.0099601 * legP)) / all_packs
    
    actualSuccessRate = shards / all_packs
    standardDeviation = math.sqrt((meanOdds * (1 - meanOdds) / all_packs))
    
    # Avoid division by zero
    if standardDeviation > 0:
        z = (actualSuccessRate - meanOdds) / standardDeviation
        probRate = stats.norm.cdf(z) * 100
        
        st.divider()
        st.subheader(f"Your Z-Score: {z:.2f}")
        
        if z > 0:
            st.success(f"You are luckier than **{probRate:.2f}%** of players.")
        else:
            st.error(f"You are unluckier than **{100 - probRate:.2f}%** of players.")
            
        st.info(f"Expected Rate: {meanOdds:.4%} | Your Rate: {actualSuccessRate:.4%}")
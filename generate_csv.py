import csv
from pathlib import Path

raw_dir = Path("data/raw")
raw_dir.mkdir(parents=True, exist_ok=True)
csv_file = raw_dir / "netflix_titles.csv"

headers = [
    "show_id", "type", "title", "director", "cast", "country",
    "date_added", "release_year", "rating", "duration", "listed_in", "description"
]

rows = [
    # Global & Western Titles
    [
        "s1", "Movie", "Dick Johnson Is Dead", "Kirsten Johnson", "", "United States",
        "September 25, 2021", 2020, "PG-13", "90 min", "Documentaries",
        "As her father nears the end of his life filmmaker Kirsten Johnson stages his death in inventive ways."
    ],
    [
        "s2", "TV Show", "Blood & Water", "", "Ama Qamata, Khosi Ngema, Gail Mabalane, Thabang Molaba", "South Africa",
        "September 24, 2021", 2021, "TV-MA", "2 Seasons", "International TV Shows, TV Dramas, TV Mysteries",
        "After crossing paths at a party a Cape Town teen sets out to prove whether a swimming star is her sister."
    ],
    [
        "s3", "TV Show", "Ganglands", "Julien Leclercq", "Sami Bouajila, Tracy Gotoas, Samuel Jouy", "France",
        "September 24, 2021", 2021, "TV-MA", "1 Season", "Crime TV Shows, International TV Shows, TV Action & Adventure",
        "To protect his family from a powerful drug lord skilled thief Mehdi and his team are pulled into a turf war."
    ],
    [
        "s4", "TV Show", "Jailbirds New Orleans", "", "", "United States",
        "September 24, 2021", 2021, "TV-MA", "1 Season", "Docuseries, Reality TV",
        "Feuds flirtations and drama go down among the incarcerated women at the Orleans Justice Center."
    ],
    [
        "s5", "TV Show", "Midnight Mass", "Mike Flanagan", "Kate Siegel, Zach Gilford, Hamish Linklater, Henry Thomas", "United States",
        "September 24, 2021", 2021, "TV-MA", "1 Season", "TV Dramas, TV Horror, TV Mysteries",
        "The arrival of a charismatic young priest brings glorious miracles and renewed religious fervor to a dying town."
    ],
    [
        "s6", "Movie", "My Little Pony: A New Generation", "Robert Cullen, Jose Luis Ucha", "Vanessa Hudgens, Kimiko Glenn, James Marsden", "United States",
        "September 24, 2021", 2021, "PG", "91 min", "Children & Family Movies, Comedies",
        "Equestria is divided. But a bright-eyed hero believes Earth Ponies Pegasi and Unicorns should be pals."
    ],
    [
        "s7", "Movie", "Sankofa", "Haile Gerima", "Kofi Ghanaba, Oyafunmike Ogunlano, Alexandra Duah", "United States, Ghana, United Kingdom",
        "September 24, 2021", 1993, "TV-MA", "125 min", "Dramas, Independent Movies, International Movies",
        "On a photo shoot in Ghana an American model has a harrowing journey back in time."
    ],
    [
        "s8", "TV Show", "The Great British Baking Show", "Andy Devonshire", "Mel Giedroyc, Sue Perkins, Mary Berry", "United Kingdom",
        "September 24, 2021", 2021, "TV-14", "9 Seasons", "British TV Shows, Reality TV",
        "A talented batch of amateur bakers face off in a 10-week competition whipping up their best dishes."
    ],
    [
        "s9", "Movie", "The Starling", "Theodore Melfi", "Melissa McCarthy, Chris O'Dowd, Kevin Kline", "United States",
        "September 24, 2021", 2021, "PG-13", "103 min", "Comedies, Dramas",
        "A woman adjusting to life after a loss contends with a feisty bird that has taken over her garden."
    ],
    [
        "s10", "TV Show", "Vendetta: Truth, Lies and The Mafia", "", "", "Italy",
        "September 24, 2021", 2021, "TV-MA", "1 Season", "Crime TV Shows, Docuseries, International TV Shows",
        "This docuseries examines the true story behind two of Sicily's most prominent anti-Mafia figures."
    ],
    [
        "s11", "TV Show", "Bangkok Breaking", "Kongkiat Komesiri", "Sukollawat Kanarot, Sushar Manaying", "Thailand",
        "September 23, 2021", 2021, "TV-MA", "1 Season", "Crime TV Shows, International TV Shows, TV Action & Adventure",
        "Newly arrived in Bangkok a wrestler teams up with a reporter to unravel a city-wide conspiracy."
    ],
    [
        "s12", "Movie", "Je Suis Karl", "Christian Schwochow", "Luna Wedler, Jannis Niewöhner, Milan Peschel", "Germany",
        "September 23, 2021", 2021, "TV-MA", "127 min", "Dramas, International Movies",
        "After her family is murdered in a bombing a young woman is lured into joining the very group responsible."
    ],
    [
        "s13", "TV Show", "Dear White People", "Justin Simien", "Logan Browning, Brandon P. Bell, DeRon Horton", "United States",
        "September 22, 2021", 2021, "TV-MA", "4 Seasons", "TV Comedies, TV Dramas",
        "Students of color navigate the daily slights and politics of life at an Ivy League college."
    ],
    [
        "s14", "Movie", "Confessions of an Invisible Girl", "Bruno Garotti", "Klara Castanho, Lucca Picon, Júlia Gomes", "Brazil",
        "September 22, 2021", 2021, "TV-PG", "91 min", "Children & Family Movies, Comedies",
        "When clever Tetê joins a new school she will do anything to fit in with her classmates."
    ],
    [
        "s15", "Movie", "Intrusion", "Adam Salky", "Freida Pinto, Logan Marshall-Green, Robert John Burke", "United States",
        "September 22, 2021", 2021, "TV-14", "93 min", "Thrillers",
        "After a deadly home invasion at a couple's new dream home the traumatized wife searches for answers."
    ],
    [
        "s16", "TV Show", "Jaguar", "", "Blanca Suárez, Iván Marcos, Francesc Garrido", "Spain",
        "September 22, 2021", 2021, "TV-MA", "1 Season", "International TV Shows, Spanish-Language TV Shows, TV Action & Adventure",
        "In the 1960s a Holocaust survivor joins a group seeking justice against Nazis who fled to Spain."
    ],
    [
        "s17", "Movie", "Europe's Most Dangerous Man", "Pedro de Echave García", "", "Spain",
        "September 22, 2021", 2020, "TV-MA", "67 min", "Documentaries, International Movies",
        "Declassified documents shed light on the post-WWII life of Otto Skorzeny in Spain."
    ],
    [
        "s18", "TV Show", "Resurrection: Ertugrul", "", "Engin Altan Düzyatan, Serdar Gökhan, Esra Bilgiç", "Turkey",
        "September 22, 2021", 2018, "TV-14", "5 Seasons", "International TV Shows, TV Action & Adventure, TV Dramas",
        "When a good deed endangers his clan a 13th-century Ottoman warrior agrees to fight the sultan's enemies."
    ],
    [
        "s19", "Movie", "Inception", "Christopher Nolan", "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page, Tom Hardy", "United States",
        "September 15, 2021", 2010, "PG-13", "148 min", "Action & Adventure, Sci-Fi & Fantasy, Thrillers",
        "A thief who steals corporate secrets through dream-sharing is given the task of planting an idea."
    ],
    [
        "s20", "Movie", "The Dark Knight", "Christopher Nolan", "Christian Bale, Heath Ledger, Aaron Eckhart, Michael Caine", "United States",
        "August 1, 2021", 2008, "PG-13", "152 min", "Action & Adventure, Dramas",
        "When the Joker wreaks havoc on Gotham Batman must accept one of the greatest tests of his ability."
    ],
    [
        "s21", "TV Show", "Stranger Things", "The Duffer Brothers", "Millie Bobby Brown, Finn Wolfhard, Winona Ryder, David Harbour", "United States",
        "May 27, 2022", 2022, "TV-14", "4 Seasons", "Sci-Fi & Fantasy, TV Dramas, TV Horror",
        "When a young boy vanishes a small town uncovers a mystery involving supernatural forces."
    ],
    [
        "s22", "TV Show", "Squid Game", "Hwang Dong-hyuk", "Lee Jung-jae, Park Hae-soo, Wi Ha-jun, Jung Ho-yeon", "South Korea",
        "September 17, 2021", 2021, "TV-MA", "2 Seasons", "International TV Shows, TV Dramas, TV Thrillers",
        "Hundreds of cash-strapped players accept a strange invitation to compete in children's games with deadly stakes."
    ],
    [
        "s23", "Movie", "Roma", "Alfonso Cuarón", "Yalitza Aparicio, Marina de Tavira, Diego Cortina Autrey", "Mexico",
        "December 14, 2018", 2018, "R", "135 min", "Dramas, Independent Movies, International Movies",
        "A year in the life of a middle-class family's maid in Mexico City in the early 1970s."
    ],
    [
        "s24", "Movie", "Interstellar", "Christopher Nolan", "Matthew McConaughey, Anne Hathaway, Jessica Chastain", "United States",
        "December 1, 2020", 2014, "PG-13", "169 min", "Action & Adventure, Dramas, Sci-Fi & Fantasy",
        "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."
    ],
    [
        "s25", "TV Show", "Money Heist", "Álex Pina", "Úrsula Corberó, Álvaro Morte, Itziar Ituño, Pedro Alonso", "Spain",
        "December 3, 2021", 2021, "TV-MA", "5 Seasons", "Crime TV Shows, International TV Shows, Spanish-Language TV Shows",
        "An unusual group of robbers attempt to carry out the most perfect robbery in Spanish history."
    ],
    [
        "s26", "Movie", "Spirited Away", "Hayao Miyazaki", "Rumi Hiiragi, Miyu Irino, Mari Natsuki", "Japan",
        "March 1, 2020", 2001, "PG", "125 min", "Anime Features, Children & Family Movies, Sci-Fi & Fantasy",
        "A 10-year-old girl wanders into a world ruled by gods witches and spirits."
    ],
    [
        "s27", "TV Show", "Breaking Bad", "Vince Gilligan", "Bryan Cranston, Aaron Paul, Anna Gunn, Dean Norris", "United States",
        "August 2, 2013", 2013, "TV-MA", "5 Seasons", "Crime TV Shows, TV Dramas, TV Thrillers",
        "A chemistry teacher diagnosed with cancer turns to manufacturing methamphetamine with a former student."
    ],
    [
        "s28", "Movie", "Parasite", "Bong Joon Ho", "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong, Choi Woo-shik", "South Korea",
        "October 11, 2019", 2019, "R", "132 min", "Comedies, Dramas, International Movies, Thrillers",
        "Greed and class discrimination threaten the symbiotic relationship between two contrasting families."
    ],
    [
        "s29", "Movie", "The Irishman", "Martin Scorsese", "Robert De Niro, Al Pacino, Joe Pesci, Harvey Keitel", "United States",
        "November 27, 2019", 2019, "R", "209 min", "Crime TV Shows, Dramas",
        "Hit man Frank Sheeran looks back at the secrets he kept as a loyal member of the Bufalino family."
    ],
    [
        "s30", "Movie", "Extraction", "Sam Hargrave", "Chris Hemsworth, Rudhraksh Jaiswal, Randeep Hooda", "United States",
        "April 24, 2020", 2020, "R", "117 min", "Action & Adventure",
        "A hardened mercenary's mission becomes a race to survive when sent to rescue a kidnapped son."
    ],
    [
        "s31", "Movie", "Bird Box", "Susanne Bier", "Sandra Bullock, Trevante Rhodes, John Malkovich", "United States",
        "December 21, 2018", 2018, "R", "124 min", "Dramas, Sci-Fi & Fantasy, Thrillers",
        "Years after an unseen presence drives society to suicide a mother and children seek sanctuary."
    ],
    [
        "s32", "TV Show", "Dark", "Baran bo Odar", "Louis Hofmann, Oliver Masucci, Jördis Triebel", "Germany",
        "June 27, 2020", 2020, "TV-MA", "3 Seasons", "Crime TV Shows, International TV Shows, TV Dramas, TV Sci-Fi & Fantasy",
        "A family saga with a supernatural twist set in a German town with mysterious disappearances."
    ],
    [
        "s33", "Movie", "Marriage Story", "Noah Baumbach", "Scarlett Johansson, Adam Driver, Laura Dern", "United States",
        "December 6, 2019", 2019, "R", "137 min", "Comedies, Dramas, Independent Movies",
        "An incisive and compassionate look at a marriage breaking up and a family staying together."
    ],
    [
        "s34", "TV Show", "The Crown", "Peter Morgan", "Claire Foy, Olivia Colman, Imelda Staunton, Matt Smith", "United Kingdom",
        "November 15, 2020", 2020, "TV-MA", "6 Seasons", "British TV Shows, TV Dramas, TV Historical",
        "Follows the political rivalries and romance of Queen Elizabeth II's reign."
    ],
    [
        "s35", "Movie", "Red Notice", "Rawson Marshall Thurber", "Dwayne Johnson, Ryan Reynolds, Gal Gadot", "United States",
        "November 12, 2021", 2021, "PG-13", "118 min", "Action & Adventure, Comedies",
        "An FBI profiler pursuing the world's most wanted art thief becomes his reluctant partner."
    ],
    [
        "s36", "TV Show", "The Queen's Gambit", "Scott Frank", "Anya Taylor-Joy, Bill Camp, Marielle Heller", "United States",
        "October 23, 2020", 2020, "TV-MA", "1 Season", "TV Dramas",
        "Orphaned at nine prodigious introvert Beth Harmon discovers and masters the game of chess."
    ],
    [
        "s37", "Movie", "The Social Dilemma", "Jeff Orlowski", "Skyler Gisondo, Kara Hayward, Vincent Kartheiser", "United States",
        "September 9, 2020", 2020, "PG-13", "94 min", "Documentaries",
        "Explores the dangerous human impact of social networking with tech experts sounding the alarm."
    ],
    [
        "s38", "Movie", "Klaus", "Sergio Pablos", "Jason Schwartzman, J.K. Simmons, Rashida Jones", "Spain",
        "November 15, 2019", 2019, "PG", "98 min", "Children & Family Movies, Comedies",
        "A selfish postman and a reclusive toymaker form an unlikely friendship delivering joy."
    ],
    [
        "s39", "TV Show", "Demon Slayer", "Haruo Sotozaki", "Natsuki Hanae, Akari Kito, Hiro Shimono", "Japan",
        "January 22, 2021", 2021, "TV-14", "4 Seasons", "Anime Series, International TV Shows",
        "Tanjiro sets out on a perilous journey to find a cure for his demon sister."
    ],
    [
        "s40", "Movie", "Don't Look Up", "Adam McKay", "Leonardo DiCaprio, Jennifer Lawrence, Meryl Streep", "United States",
        "December 24, 2021", 2021, "R", "138 min", "Comedies, Dramas, Sci-Fi & Fantasy",
        "Two astronomers go on a giant media tour to warn mankind of an approaching comet."
    ],
    [
        "s41", "TV Show", "Narcos", "Carlo Bernard", "Wagner Moura, Pedro Pascal, Boyd Holbrook", "United States",
        "September 1, 2017", 2017, "TV-MA", "3 Seasons", "Crime TV Shows, TV Action & Adventure, TV Dramas",
        "A chronicle of the war against drug cartels and the rise and fall of Pablo Escobar."
    ],
    [
        "s42", "Movie", "Guillermo del Toro's Pinocchio", "Guillermo del Toro", "Ewan McGregor, David Bradley, Gregory Mann", "United States",
        "December 9, 2022", 2022, "PG", "117 min", "Animation, Children & Family Movies, Dramas",
        "Reinvents the classic story of a wooden puppet brought to life in stop-motion."
    ],
    [
        "s43", "Movie", "Glass Onion", "Rian Johnson", "Daniel Craig, Edward Norton, Janelle Monáe", "United States",
        "December 23, 2022", 2022, "PG-13", "140 min", "Comedies, Crime Movies, Dramas",
        "Detective Benoit Blanc heads to Greece to peel back the layers of a mystery."
    ],
    [
        "s44", "TV Show", "Wednesday", "Tim Burton", "Jenna Ortega, Gwendoline Christie, Riki Lindhome", "United States",
        "November 23, 2022", 2022, "TV-14", "2 Seasons", "TV Comedies, TV Mysteries, TV Sci-Fi & Fantasy",
        "Wednesday Addams investigates a murder spree while making friends and foes at Nevermore."
    ],
    [
        "s45", "TV Show", "Cyberpunk: Edgerunners", "Hiroyuki Imaishi", "KENN, Aoi Yuuki, Hiroki Touchi", "Japan",
        "September 13, 2022", 2022, "TV-MA", "1 Season", "Action & Adventure, Anime Series, Sci-Fi & Fantasy",
        "A street kid trying to survive in a body-modification obsessed city becomes an outlaw."
    ],
    [
        "s46", "Movie", "All Quiet on the Western Front", "Edward Berger", "Felix Kammerer, Albrecht Schuch", "Germany",
        "October 28, 2022", 2022, "R", "148 min", "Action & Adventure, Dramas, International Movies",
        "A young soldier on the Western Front faces the grim reality of life in the trenches."
    ],
    [
        "s47", "TV Show", "Alice in Borderland", "Shinsuke Sato", "Kento Yamazaki, Tao Tsuchiya", "Japan",
        "December 22, 2022", 2022, "TV-MA", "3 Seasons", "International TV Shows, TV Action & Adventure, TV Sci-Fi & Fantasy",
        "An aimless gamer finds himself in a parallel Tokyo competing in sadistic games to survive."
    ],
    [
        "s48", "Movie", "Enola Holmes", "Harry Bradbeer", "Millie Bobby Brown, Henry Cavill, Sam Claflin", "United Kingdom",
        "September 23, 2020", 2020, "PG-13", "124 min", "Action & Adventure, Children & Family Movies, Comedies",
        "Searching for her mother teen Enola Holmes uses sleuthing skills to outsmart big brother Sherlock."
    ],
    [
        "s49", "TV Show", "Lupin", "George Kay", "Omar Sy, Ludivine Sagnier, Clotilde Hesme", "France",
        "June 11, 2021", 2021, "TV-MA", "3 Seasons", "Crime TV Shows, International TV Shows, TV Dramas",
        "Gentleman thief Assane Diop sets out to avenge his father for an injustice."
    ],
    [
        "s50", "TV Show", "Peaky Blinders", "Steven Knight", "Cillian Murphy, Sam Neill, Helen McCrory", "United Kingdom",
        "June 10, 2022", 2022, "TV-MA", "6 Seasons", "British TV Shows, Crime TV Shows, TV Dramas",
        "A gang in 1919 Birmingham is led by the fierce Tommy Shelby moving up in the world."
    ],
    [
        "s51", "TV Show", "Cobra Kai", "Josh Heald", "Ralph Macchio, William Zabka, Xolo Maridueña", "United States",
        "September 9, 2022", 2022, "TV-14", "6 Seasons", "TV Action & Adventure, TV Comedies, TV Dramas",
        "Decades after the tournament rivalry reignites between Johnny and Daniel."
    ],
    [
        "s52", "Movie", "The Adam Project", "Shawn Levy", "Ryan Reynolds, Mark Ruffalo, Jennifer Garner", "United States",
        "March 11, 2022", 2022, "PG-13", "106 min", "Action & Adventure, Children & Family Movies, Sci-Fi & Fantasy",
        "Time-traveling fighter pilot Adam Reed teams up with his 12-year-old self."
    ],
    [
        "s53", "TV Show", "Ozark", "Bill Dubuque", "Jason Bateman, Laura Linney, Julia Garner", "United States",
        "April 29, 2022", 2022, "TV-MA", "4 Seasons", "Crime TV Shows, TV Dramas, TV Thrillers",
        "A financial adviser drags his family to the Missouri Ozarks to launder 500 million dollars."
    ],
    [
        "s54", "TV Show", "Lucifer", "Tom Kapinos", "Tom Ellis, Lauren German, Kevin Alejandro", "United States",
        "September 10, 2021", 2021, "TV-14", "6 Seasons", "Crime TV Shows, TV Comedies, TV Sci-Fi & Fantasy",
        "Bored with being the Lord of Hell the devil relocates to Los Angeles to assist police."
    ],
    [
        "s55", "Movie", "Society of the Snow", "J.A. Bayona", "Enzo Vogrincic, Agustín Pardella", "Spain",
        "January 4, 2024", 2023, "R", "144 min", "Action & Adventure, Dramas, International Movies",
        "In 1972 a rugby team's flight crashes into a glacier in the heart of the Andes."
    ],
    [
        "s56", "TV Show", "One Piece", "Matt Owens", "Iñaki Godoy, Emily Rudd, Mackenyu", "United States",
        "August 31, 2023", 2023, "TV-14", "2 Seasons", "Action & Adventure, TV Comedies, TV Sci-Fi & Fantasy",
        "Young pirate Monkey D. Luffy goes on an epic voyage for treasure in this live-action adaptation."
    ],
    [
        "s57", "Movie", "The Boy and the Heron", "Hayao Miyazaki", "Soma Santoki, Masaki Suda", "Japan",
        "October 7, 2023", 2023, "PG-13", "124 min", "Anime Features, Children & Family Movies, Sci-Fi & Fantasy",
        "A 12-year-old boy follows a mysterious gray heron into a world shared by the living and the dead."
    ],
    [
        "s58", "Movie", "Leave the World Behind", "Sam Esmail", "Julia Roberts, Mahershala Ali, Ethan Hawke", "United States",
        "December 8, 2023", 2023, "R", "141 min", "Dramas, Sci-Fi & Fantasy, Thrillers",
        "A family's quiet getaway is upended when two strangers arrive bearing news of a cyberattack."
    ],
    [
        "s59", "TV Show", "The Witcher", "Lauren Schmidt Hissrich", "Henry Cavill, Anya Chalotra, Freya Allan", "United States",
        "July 27, 2023", 2023, "TV-MA", "4 Seasons", "Action & Adventure, TV Dramas, TV Sci-Fi & Fantasy",
        "Geralt of Rivia a mutated monster-hunter journeys toward his destiny."
    ],
    [
        "s60", "TV Show", "Heartstopper", "Alice Oseman", "Joe Locke, Kit Connor, William Gao", "United Kingdom",
        "August 3, 2023", 2023, "TV-14", "3 Seasons", "British TV Shows, Romantic TV Shows, TV Dramas",
        "Teens Charlie and Nick discover their unlikely friendship might be something more."
    ],
    [
        "s61", "Movie", "Nimona", "Nick Bruno, Troy Quane", "Chloë Grace Moretz, Riz Ahmed", "United States",
        "June 30, 2023", 2023, "PG", "101 min", "Action & Adventure, Children & Family Movies, Comedies",
        "A knight framed for a crime is helped by a mischievous shapeshifting teen."
    ],
    [
        "s62", "Movie", "Dune: Part Two", "Denis Villeneuve", "Timothée Chalamet, Zendaya, Rebecca Ferguson", "United States",
        "March 15, 2024", 2024, "PG-13", "166 min", "Action & Adventure, Sci-Fi & Fantasy, Dramas",
        "Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators."
    ],
    [
        "s63", "Movie", "Deadpool & Wolverine", "Shawn Levy", "Ryan Reynolds, Hugh Jackman, Emma Corrin", "United States",
        "July 26, 2024", 2024, "R", "128 min", "Action & Adventure, Comedies, Sci-Fi & Fantasy",
        "Wolverine is recovering from his injuries when he crosses paths with the loudmouth Deadpool."
    ],
    [
        "s64", "TV Show", "3 Body Problem", "David Benioff, D.B. Weiss", "Benedict Wong, Jess Hong, Jovan Adepo", "United States",
        "March 21, 2024", 2024, "TV-MA", "1 Season", "TV Dramas, TV Mysteries, TV Sci-Fi & Fantasy",
        "A fateful decision made in 1960s China reverberates across space and time to a group of scientists in the present."
    ],
    [
        "s65", "TV Show", "Avatar: The Last Airbender", "Albert Kim", "Gordon Cormier, Kiawentiio, Ian Ousley, Dallas Liu", "United States",
        "February 22, 2024", 2024, "TV-PG", "1 Season", "Action & Adventure, Children & Family Movies, TV Sci-Fi & Fantasy",
        "A young boy known as the Avatar must master the four elemental powers to save a world at war."
    ],

    # ==========================================
    # INDIAN MOVIES (Classic, Modern & up to 2026)
    # ==========================================
    [
        "s66", "Movie", "Lagaan: Once Upon a Time in India", "Ashutosh Gowariker", "Aamir Khan, Gracy Singh, Rachel Shelley", "India",
        "January 15, 2018", 2001, "PG", "224 min", "Dramas, International Movies, Sports Movies",
        "In Victorian India a resilient farmer challenges British officers to a game of cricket to avoid crippling taxes."
    ],
    [
        "s67", "Movie", "Swades", "Ashutosh Gowariker", "Shah Rukh Khan, Gayatri Joshi, Kishori Ballal", "India",
        "December 17, 2017", 2004, "TV-PG", "210 min", "Dramas, International Movies",
        "A successful NASA project manager returns to his native village in India to find his childhood nanny."
    ],
    [
        "s68", "Movie", "Taare Zameen Par", "Aamir Khan", "Aamir Khan, Darsheel Safary, Tisca Chopra", "India",
        "August 15, 2018", 2007, "PG", "165 min", "Children & Family Movies, Dramas, International Movies",
        "An eight-year-old boy is thought to be lazy and troublesome until the new art teacher discovers his true struggle."
    ],
    [
        "s69", "Movie", "3 Idiots", "Rajkumar Hirani", "Aamir Khan, Kareena Kapoor, R. Madhavan, Sharman Joshi", "India",
        "August 1, 2019", 2009, "PG-13", "164 min", "Comedies, Dramas, International Movies, Romantic Movies",
        "Two friends search for their long-lost college buddy while recalling their days at an elite engineering institute."
    ],
    [
        "s70", "Movie", "PK", "Rajkumar Hirani", "Aamir Khan, Anushka Sharma, Sushant Singh Rajput, Sanjay Dutt", "India",
        "May 1, 2018", 2014, "TV-PG", "153 min", "Comedies, Dramas, International Movies, Sci-Fi & Fantasy",
        "An innocent alien stranded on Earth loses his remote control communication device and questions blind faith dogma."
    ],
    [
        "s71", "Movie", "Baahubali: The Beginning", "S.S. Rajamouli", "Prabhas, Rana Daggubati, Anushka Shetty, Tamannaah Bhatia", "India",
        "August 10, 2017", 2015, "TV-14", "159 min", "Action & Adventure, Dramas, International Movies",
        "In ancient India an adventurous young man becomes embroiled in a bitter battle between two warring brothers."
    ],
    [
        "s72", "Movie", "Dangal", "Nitesh Tiwari", "Aamir Khan, Sakshi Tanwar, Fatima Sana Shaikh, Sanya Malhotra", "India",
        "June 21, 2017", 2016, "TV-PG", "161 min", "Action & Adventure, Dramas, International Movies, Sports Movies",
        "Former wrestler Mahavir Singh Phogat trains his young daughters Geeta and Babita to become world-class champions."
    ],
    [
        "s73", "Movie", "Baahubali 2: The Conclusion", "S.S. Rajamouli", "Prabhas, Rana Daggubati, Anushka Shetty, Ramya Krishnan", "India",
        "September 1, 2017", 2017, "TV-14", "167 min", "Action & Adventure, Dramas, International Movies",
        "When Shiva discovers his royal heritage he seeks vengeance for his father's betrayal and redeems the kingdom."
    ],
    [
        "s74", "Movie", "Andhadhun", "Sriram Raghavan", "Ayushmann Khurrana, Tabu, Radhika Apte, Anil Dhawan", "India",
        "December 15, 2018", 2018, "TV-MA", "139 min", "Comedies, Crime Movies, International Movies, Thrillers",
        "A series of mysterious events unfold when a piano player pretending to be blind inadvertently witnesses a homicide."
    ],
    [
        "s75", "Movie", "Stree", "Amar Kaushik", "Rajkummar Rao, Shraddha Kapoor, Pankaj Tripathi, Aparshakti Khurana", "India",
        "January 1, 2019", 2018, "TV-14", "128 min", "Comedies, Horror Movies, International Movies",
        "In the small town of Chanderi men live in terror of an evil female spirit who abducts young men at night during festivals."
    ],
    [
        "s76", "Movie", "Super 30", "Vikas Bahl", "Hrithik Roshan, Mrunal Thakur, Nandish Sandhu, Pankaj Tripathi", "India",
        "October 10, 2019", 2019, "TV-14", "154 min", "Dramas, Educational Movies, International Movies",
        "Genius mathematician Anand Kumar starts the Super 30 educational program to coach underprivileged students for IIT entrance."
    ],
    [
        "s77", "Movie", "Ludo", "Anurag Basu", "Abhishek Bachchan, Aditya Roy Kapur, Rajkummar Rao, Pankaj Tripathi", "India",
        "November 12, 2020", 2020, "TV-MA", "150 min", "Comedies, Crime Movies, Dramas, International Movies",
        "From a resurrected sex tape to a rogue suitcase of money four wildly different stories overlap at the whims of fate."
    ],
    [
        "s78", "Movie", "Mimi", "Laxman Utekar", "Kriti Sanon, Pankaj Tripathi, Sai Tamhankar, Manoj Pahwa", "India",
        "July 26, 2021", 2021, "TV-PG", "132 min", "Comedies, Dramas, International Movies",
        "An aspiring actress in a small town agrees to bear a child for a visiting American couple for a hefty payout."
    ],
    [
        "s79", "Movie", "Shershaah", "Vishnuvardhan", "Sidharth Malhotra, Kiara Advani, Shiv Panditt", "India",
        "August 12, 2021", 2021, "TV-14", "135 min", "Action & Adventure, Dramas, International Movies",
        "The inspiring life story of Indian Army Captain Vikram Batra PVC who fought heroically in the 1999 Kargil War."
    ],
    [
        "s80", "Movie", "RRR", "S.S. Rajamouli", "N.T. Rama Rao Jr., Ram Charan, Ajay Devgn, Alia Bhatt", "India",
        "May 20, 2022", 2022, "TV-MA", "187 min", "Action & Adventure, Dramas, International Movies",
        "A fearless tribal guardian on a rescue mission clashes with an ambitious police officer serving the British Raj."
    ],
    [
        "s81", "Movie", "Gangubai Kathiawadi", "Sanjay Leela Bhansali", "Alia Bhatt, Shantanu Maheshwari, Vijay Raaz, Ajay Devgn", "India",
        "April 26, 2022", 2022, "TV-MA", "152 min", "Crime Movies, Dramas, International Movies",
        "Dupe-sold into prostitution a fierce young woman rises to power in Kamathipura becoming a champion for sex workers rights."
    ],
    [
        "s82", "Movie", "Brahmāstra: Part One – Shiva", "Ayan Mukerji", "Ranbir Kapoor, Alia Bhatt, Amitabh Bachchan, Nagarjuna", "India",
        "November 4, 2022", 2022, "TV-14", "167 min", "Action & Adventure, Sci-Fi & Fantasy, International Movies",
        "A young disc jockey discovers his mysterious supernatural connection with fire and the ancient secret society of Astraverse."
    ],
    [
        "s83", "Movie", "Kantara", "Rishab Shetty", "Rishab Shetty, Sapthami Gowda, Kishore", "India",
        "December 9, 2022", 2022, "TV-MA", "148 min", "Action & Adventure, Dramas, International Movies, Thrillers",
        "When greed paves the way for betrayal a tribal champion summons the divine wrath of Daiva spirit to protect his sacred village."
    ],
    [
        "s84", "Movie", "Drishyam 2", "Abhishek Pathak", "Ajay Devgn, Tabu, Akshaye Khanna, Shriya Saran", "India",
        "January 13, 2023", 2022, "TV-14", "140 min", "Crime Movies, Dramas, International Movies, Thrillers",
        "Seven years after the original case is closed a gripping series of unexpected clues threatens to uncover Vijay Salgaonkar family."
    ],
    [
        "s85", "Movie", "Jawan", "Atlee", "Shah Rukh Khan, Nayanthara, Vijay Sethupathi, Deepika Padukone", "India",
        "November 2, 2023", 2023, "TV-14", "169 min", "Action & Adventure, Dramas, International Movies, Thrillers",
        "A driven prison warden backed by a squad of righteous female inmates takes on systemic government corruption."
    ],
    [
        "s86", "Movie", "Animal", "Sandeep Reddy Vanga", "Ranbir Kapoor, Anil Kapoor, Rashmika Mandanna, Bobby Deol", "India",
        "January 26, 2024", 2023, "TV-MA", "204 min", "Action & Adventure, Crime Movies, Dramas, International Movies",
        "A hardened son embarks on a brutal blood-soaked path of vengeance when an assassination attempt is made on his estranged father."
    ],
    [
        "s87", "Movie", "Dunki", "Rajkumar Hirani", "Shah Rukh Khan, Taapsee Pannu, Vicky Kaushal, Boman Irani", "India",
        "February 15, 2024", 2023, "TV-14", "161 min", "Comedies, Dramas, International Movies",
        "Four friends from a Punjab village dream of migrating to England and attempt an unconventional journey known as the Donkey Flight."
    ],
    [
        "s88", "Movie", "12th Fail", "Vidhu Vinod Chopra", "Vikrant Massey, Medha Shankr, Anant Joshi, Priyanshu Chatterjee", "India",
        "December 29, 2023", 2023, "TV-14", "147 min", "Dramas, Educational Movies, International Movies",
        "Based on true events Manoj Kumar Sharma battles extreme poverty and multiple failures to clear the coveted UPSC examination."
    ],
    [
        "s89", "Movie", "Salaar: Part 1 – Ceasefire", "Prashanth Neel", "Prabhas, Prithviraj Sukumaran, Shruti Haasan, Jagapathi Babu", "India",
        "January 20, 2024", 2023, "TV-MA", "175 min", "Action & Adventure, Crime Movies, International Movies",
        "In the lawless walled city-state of Khansaar childhood best friends turn from comrades into lethal adversaries over absolute power."
    ],
    [
        "s90", "Movie", "Jailer", "Nelson Dilipkumar", "Rajinikanth, Vinayakan, Ramya Krishnan, Vasanth Ravi", "India",
        "September 7, 2023", 2023, "TV-MA", "168 min", "Action & Adventure, Crime Movies, International Movies",
        "A retired prison warden steps back into the violent criminal underworld when his righteous policeman son mysteriously disappears."
    ],
    [
        "s91", "Movie", "Leo", "Lokesh Kanagaraj", "Thalapathy Vijay, Sanjay Dutt, Arjun Sarja, Trisha Krishnan", "India",
        "November 24, 2023", 2023, "TV-MA", "164 min", "Action & Adventure, Crime Movies, International Movies, Thrillers",
        "A peaceful cafe owner in Himachal Pradesh is targeted by a ruthless cartel who suspect he is their former enforcer."
    ],
    [
        "s92", "Movie", "Maharaja", "Nithilan Saminathan", "Vijay Sethupathi, Anurag Kashyap, Mamta Mohandas, Natarajan", "India",
        "July 12, 2024", 2024, "TV-MA", "141 min", "Action & Adventure, Crime Movies, International Movies, Thrillers",
        "A humble barber approaches the local police precinct reporting that his domestic metal bin was stolen, hiding a darker tragedy."
    ],
    [
        "s93", "Movie", "Amar Singh Chamkila", "Imtiaz Ali", "Diljit Dosanjh, Parineeti Chopra, Anurag Arora", "India",
        "April 12, 2024", 2024, "TV-MA", "145 min", "Dramas, International Movies, Music & Musicals",
        "The meteoric rise and tragic assassination of Punjab highest-record selling rockstar singer whose bold lyrics provoked conservative outrage."
    ],
    [
        "s94", "Movie", "Laapataa Ladies", "Kiran Rao", "Nitanshi Goel, Pratibha Ranta, Sparsh Shrivastava, Ravi Kishan", "India",
        "April 26, 2024", 2024, "TV-14", "122 min", "Comedies, Dramas, International Movies",
        "In rural central India two newlywed brides are accidentally swapped on a crowded passenger train sparking a heartfelt search."
    ],
    [
        "s95", "Movie", "Fighter", "Siddharth Anand", "Hrithik Roshan, Deepika Padukone, Anil Kapoor, Karan Singh Grover", "India",
        "March 21, 2024", 2024, "TV-14", "166 min", "Action & Adventure, Dramas, International Movies",
        "Top Indian Air Force fighter pilots form an elite special task unit called Air Dragons to combat cross-border aerial warfare."
    ],
    [
        "s96", "Movie", "Kalki 2898 AD", "Nag Ashwin", "Prabhas, Amitabh Bachchan, Kamal Haasan, Deepika Padukone", "India",
        "August 22, 2024", 2024, "TV-14", "181 min", "Action & Adventure, Sci-Fi & Fantasy, International Movies",
        "In a dystopian post-apocalyptic world ruled by Supreme Yaskin immortal warrior Ashwatthama awakens to protect the prophesied avatar."
    ],
    [
        "s97", "Movie", "Stree 2", "Amar Kaushik", "Rajkummar Rao, Shraddha Kapoor, Pankaj Tripathi, Abhishek Banerjee", "India",
        "October 11, 2024", 2024, "TV-14", "147 min", "Comedies, Horror Movies, International Movies",
        "The spirited residents of Chanderi unite with the legendary Stree spirit to battle a decapitated demon terrorizing progressive women."
    ],
    [
        "s98", "Movie", "Bhool Bhulaiyaa 3", "Anees Bazmee", "Kartik Aaryan, Vidya Balan, Madhuri Dixit, Triptii Dimri", "India",
        "December 20, 2024", 2024, "TV-14", "158 min", "Comedies, Horror Movies, International Movies",
        "Charismatic psychic fraudster Rooh Baba is summoned to an ancestral fortress in Bengal where two royal spirits wage a haunted war."
    ],
    [
        "s99", "Movie", "Pushpa 2: The Rule", "Sukumar", "Allu Arjun, Rashmika Mandanna, Fahadh Faasil, Sunil", "India",
        "January 10, 2025", 2024, "TV-MA", "200 min", "Action & Adventure, Crime Movies, Dramas, International Movies",
        "Pushpa Raj consolidates his undisputed iron-fisted monopoly over red sandalwood smuggling while waging a clash against SP Bhanwar Singh."
    ],
    [
        "s100", "Movie", "Manjummel Boys", "Chidambaram", "Soubin Shahir, Sreenath Bhasi, Balu Varghese, Ganapathi", "India",
        "May 5, 2024", 2024, "TV-14", "135 min", "Action & Adventure, Dramas, International Movies, Thrillers",
        "A spirited group of vacationing friends from Kerala embark on a daring rescue inside the bottomless Devil Kitchen cave at Guna."
    ],
    [
        "s101", "Movie", "Aavesham", "Jithu Madhavan", "Fahadh Faasil, Hipzster, Mithun Jai Shankar, Roshan Shanavas", "India",
        "May 17, 2024", 2024, "TV-MA", "158 min", "Action & Adventure, Comedies, International Movies",
        "Three engineering college freshmen in Bengaluru seek out an eccentric local gangster named Ranga to handle their campus bullies."
    ],
    [
        "s102", "Movie", "Sikandar", "AR Murugadoss", "Salman Khan, Rashmika Mandanna, Sathyaraj, Prateik Babbar", "India",
        "April 15, 2025", 2025, "TV-14", "160 min", "Action & Adventure, Dramas, International Movies",
        "A fearless vigilante champion rises from the streets of Mumbai to dismantle a transnational syndicate oppressing working-class citizens."
    ],
    [
        "s103", "Movie", "War 2", "Ayan Mukerji", "Hrithik Roshan, N.T. Rama Rao Jr., Kiara Advani, John Abraham", "India",
        "August 14, 2025", 2025, "TV-14", "165 min", "Action & Adventure, International Movies, Thrillers",
        "Major Kabir Dhaliwal confronts a rogue super-soldier operative across international hotspots in an adrenaline-pumping espionage showdown."
    ],
    [
        "s104", "Movie", "Toxic: A Fairy Tale for Grown-ups", "Geetu Mohandas", "Yash, Kiara Advani, Huma Qureshi, Nayanthara", "India",
        "December 18, 2025", 2025, "TV-MA", "170 min", "Action & Adventure, Crime Movies, Dramas, International Movies",
        "A stylish noir gangster saga set in a retro Goa underworld chronicles the intoxicating rise and lethal ambition of a shadow boss."
    ],
    [
        "s105", "Movie", "Alpha", "Shiv Rawail", "Alia Bhatt, Sharvari Wagh, Bobby Deol, Anil Kapoor", "India",
        "December 25, 2025", 2025, "TV-14", "150 min", "Action & Adventure, International Movies, Thrillers",
        "Two highly skilled female field agents lead a covert tactical operation deep inside enemy territory to prevent weapons of mass chaos."
    ],
    [
        "s106", "Movie", "Spirit", "Sandeep Reddy Vanga", "Prabhas, Triptii Dimri, Vivek Oberoi, Prakash Raj", "India",
        "February 20, 2026", 2026, "TV-MA", "190 min", "Action & Adventure, Crime Movies, Dramas, International Movies",
        "A hyper-focused and ruthless IPS police officer refuses to bend to political pressure while tearing down an illicit global cartel."
    ],
    [
        "s107", "Movie", "Ramayana: Part 1", "Nitesh Tiwari", "Ranbir Kapoor, Sai Pallavi, Yash, Sunny Deol", "India",
        "April 10, 2026", 2026, "TV-14", "185 min", "Action & Adventure, Dramas, Sci-Fi & Fantasy, International Movies",
        "A visually stunning and deeply emotional mythological epic recounting the virtuous early life and legendary exile of Prince Rama."
    ],
    [
        "s108", "Movie", "Animal Park", "Sandeep Reddy Vanga", "Ranbir Kapoor, Bobby Deol, Anil Kapoor, Rashmika Mandanna", "India",
        "May 15, 2026", 2026, "TV-MA", "210 min", "Action & Adventure, Crime Movies, Dramas, International Movies",
        "The high-octane continuation pits Ranvijay against his identical doppelganger Aziz in a ferocious multinational blood feud."
    ],
    [
        "s109", "Movie", "KGF: Chapter 3", "Prashanth Neel", "Yash, Sanjay Dutt, Srinidhi Shetty, Raveena Tandon", "India",
        "October 2, 2026", 2026, "TV-MA", "180 min", "Action & Adventure, Crime Movies, Dramas, International Movies",
        "The untold international chapter reveals Rocky Bhai secret maritime gold empire and confrontation with international naval armadas."
    ],

    # ==========================================
    # INDIAN TV SHOWS & SERIES (up to 2026)
    # ==========================================
    [
        "s110", "TV Show", "Sacred Games", "Vikramaditya Motwane, Anurag Kashyap", "Saif Ali Khan, Nawazuddin Siddiqui, Radhika Apte, Pankaj Tripathi", "India",
        "August 15, 2019", 2019, "TV-MA", "2 Seasons", "Crime TV Shows, International TV Shows, TV Dramas, TV Thrillers",
        "A link in their pasts leads an honest police officer to a fugitive gang boss whose cryptic warning spurs a race to save Mumbai."
    ],
    [
        "s111", "TV Show", "Delhi Crime", "Richie Mehta, Tanuj Chopra", "Shefali Shah, Rasika Dugal, Rajesh Tailang, Adil Hussain", "India",
        "August 26, 2022", 2022, "TV-MA", "2 Seasons", "Crime TV Shows, Docuseries, International TV Shows, TV Dramas",
        "Following the investigation of high-profile horrific crimes in the national capital DCP Vartika Chaturvedi leads her dedicated unit."
    ],
    [
        "s112", "TV Show", "Kota Factory", "Raghav Subbu, Pratish Mehta", "Jitendra Kumar, Mayur More, Ranjan Raj, Alam Khan, Ahsaas Channa", "India",
        "June 20, 2024", 2024, "TV-MA", "3 Seasons", "International TV Shows, Romantic TV Shows, TV Comedies, TV Dramas",
        "In a city of coaching institutions known to train India finest minds earnest teenagers navigate competitive exams under mentor Jeetu Bhaiya."
    ],
    [
        "s113", "TV Show", "Crime Stories: India Detectives", "Jack Warrender", "N. Harish, Mahesh Kumar, V. Sridhar", "India",
        "September 22, 2021", 2021, "TV-MA", "1 Season", "Crime TV Shows, Docuseries, International TV Shows",
        "Cameras follow Bengaluru City police personnel on the ground offering a rare look inside intense homicide investigations."
    ],
    [
        "s114", "TV Show", "Decoupled", "Hardik Mehta", "R. Madhavan, Surveen Chawla, Chetan Bhagat, Atul Kumar", "India",
        "December 17, 2021", 2021, "TV-MA", "1 Season", "International TV Shows, Romantic TV Shows, TV Comedies",
        "A misanthropic pulp fiction author and his corporate wife declare an impending divorce while navigating eccentric friends in Gurgaon."
    ],
    [
        "s115", "TV Show", "Yeh Kaali Kaali Ankhein", "Sidharth Sengupta", "Tahir Raj Bhasin, Shweta Tripathi, Anchal Singh, Saurabh Shukla", "India",
        "November 22, 2024", 2024, "TV-MA", "2 Seasons", "Crime TV Shows, International TV Shows, Romantic TV Shows, TV Thrillers",
        "Relentlessly pursued by a ruthless politician powerful daughter who will do anything to make him hers a timid man takes a dark path."
    ],
    [
        "s116", "TV Show", "Khakee: The Bihar Chapter", "Bhav Dhulia", "Karan Tacker, Avinash Tiwary, Abhimanyu Singh, Ravi Kishan", "India",
        "November 25, 2022", 2022, "TV-MA", "1 Season", "Crime TV Shows, International TV Shows, TV Action & Adventure, TV Dramas",
        "As a righteous IPS officer tackles a notorious outlaw in the heartland of Bihar he faces a treacherous battle against entrenched mafias."
    ],
    [
        "s117", "TV Show", "Indian Predator: The Butcher of Delhi", "Ayesha Sood", "Manjit Singh, Sanjay Bansal, Jitendra Sharma", "India",
        "July 20, 2022", 2022, "TV-MA", "1 Season", "Crime TV Shows, Docuseries, International TV Shows",
        "A string of decapitated bodies and taunting handwritten notes left outside a Delhi jail send police hunting for a remorseless serial killer."
    ],
    [
        "s118", "TV Show", "Rana Naidu", "Karan Anshuman, Suparn Verma", "Venkatesh Daggubati, Rana Daggubati, Surveen Chawla, Abhishek Banerjee", "India",
        "March 10, 2023", 2023, "TV-MA", "1 Season", "Action & Adventure, Crime TV Shows, International TV Shows, TV Dramas",
        "Rana Naidu is the premier fixer for Bollywood elite and sports superstars, but his world spirals when his estranged ex-con father is released."
    ],
    [
        "s119", "TV Show", "Guns & Gulaabs", "Raj & DK", "Rajkummar Rao, Dulquer Salmaan, Adarsh Gourav, Gulshan Devaiah", "India",
        "August 18, 2023", 2023, "TV-MA", "1 Season", "Crime TV Shows, International TV Shows, TV Action & Adventure, TV Comedies",
        "In the 1990s cartel town of Gulaabganj an unprecedented opium deal drags a lovesick mechanic, a cop, and an unhinged assassin into madness."
    ],
    [
        "s120", "TV Show", "Scoop", "Hansal Mehta", "Karishma Tanna, Mohammed Zeeshan Ayyub, Prosenjit Chatterjee, Harman Baweja", "India",
        "June 2, 2023", 2023, "TV-MA", "1 Season", "Crime TV Shows, International TV Shows, TV Dramas",
        "The shocking murder of a veteran crime journalist puts a fearless star reporter behind bars as she fights to clear her framed name."
    ],
    [
        "s121", "TV Show", "The Railway Men", "Shiv Rawail", "R. Madhavan, Kay Kay Menon, Divyenndu, Babil Khan", "India",
        "November 18, 2023", 2023, "TV-14", "1 Season", "Action & Adventure, International TV Shows, TV Dramas, TV Historical",
        "After a deadly toxic gas leaks from a pesticide factory in Bhopal brave Indian railway workers risk their lives to rescue trapped passengers."
    ],
    [
        "s122", "TV Show", "Killer Soup", "Abhishek Chaubey", "Manoj Bajpayee, Konkona Sen Sharma, Nassar, Sayaji Shinde", "India",
        "January 11, 2024", 2024, "TV-MA", "1 Season", "Crime TV Shows, International TV Shows, TV Comedies, TV Thrillers",
        "An inept aspiring chef schemes to replace her murdered husband with her lover, but a meddling police inspector threatens the broth."
    ],
    [
        "s123", "TV Show", "Heeramandi: The Diamond Bazaar", "Sanjay Leela Bhansali", "Manisha Koirala, Sonakshi Sinha, Aditi Rao Hydari, Richa Chadha", "India",
        "May 1, 2024", 2024, "TV-MA", "1 Season", "International TV Shows, Romantic TV Shows, TV Dramas, TV Historical",
        "The cunning courtesans of Lahore iconic Heeramandi district reign as queens, until love, betrayal, and the freedom movement collide."
    ],
    [
        "s124", "TV Show", "IC 814: The Kandahar Hijack", "Anubhav Sinha", "Vijay Varma, Naseeruddin Shah, Pankaj Kapur, Arvind Swamy", "India",
        "August 29, 2024", 2024, "TV-14", "1 Season", "Action & Adventure, International TV Shows, TV Dramas, TV Thrillers",
        "On Christmas Eve 1999 Indian Airlines Flight 814 is hijacked en route to Delhi, triggering India longest tense diplomatic hostage ordeal."
    ],
    [
        "s125", "TV Show", "Tribhuvan Mishra CA Topper", "Amrit Raj Gupta", "Manav Kaul, Tillotama Shome, Shweta Basu Prasad, Subhrajyoti Barat", "India",
        "July 18, 2024", 2024, "TV-MA", "1 Season", "Crime TV Shows, International TV Shows, TV Comedies, TV Dramas",
        "An upright financial accountant is driven into an eccentric side business of male escort services to pay off crushing debts."
    ],
    [
        "s126", "TV Show", "Dabba Cartel", "Hitesh Bhatia", "Shabana Azmi, Jyotika, Shalini Pandey, Nimisha Sajayan, Gajraj Rao", "India",
        "January 24, 2025", 2025, "TV-MA", "1 Season", "Crime TV Shows, International TV Shows, TV Dramas, TV Thrillers",
        "Five ordinary suburban housewives running an innocent lunchbox tiffin delivery service covertly build a high-stakes narcotics empire."
    ],
    [
        "s127", "TV Show", "Mandala Murders", "Gopi Puthran", "Vaani Kapoor, Vaibhav Raj Gupta, Surveen Chawla, Jameel Khan", "India",
        "April 18, 2025", 2025, "TV-MA", "1 Season", "Crime TV Shows, International TV Shows, TV Mysteries, TV Thrillers",
        "Two idiosyncratic detectives hunt a calculating serial killer who leaves occult geometric mandala symbols across ancient pilgrimage cities."
    ],
    [
        "s128", "TV Show", "Khakee: The Bengal Chapter", "Neeraj Pandey", "Prosenjit Chatterjee, Jeet, Parambrata Chatterjee, Saswata Chatterjee", "India",
        "September 5, 2025", 2025, "TV-MA", "1 Season", "Action & Adventure, Crime TV Shows, International TV Shows, TV Dramas",
        "In the tumultuous 1990s Kolkata ports an upright police commissioner locks horns with dockside underworld syndicates and corrupt dons."
    ],
    [
        "s129", "TV Show", "Heeramandi: Season 2", "Sanjay Leela Bhansali", "Manisha Koirala, Sonakshi Sinha, Aditi Rao Hydari, Fardeen Khan", "India",
        "February 14, 2026", 2026, "TV-MA", "2 Seasons", "International TV Shows, Romantic TV Shows, TV Dramas, TV Historical",
        "In post-partition India the surviving courtesans relocate to Bombay cinema world battling fresh rivalries for artistic supremacy."
    ],
    [
        "s130", "TV Show", "Delhi Crime: Season 3", "Tanuj Chopra", "Shefali Shah, Rasika Dugal, Rajesh Tailang, Tillotama Shome", "India",
        "April 24, 2026", 2026, "TV-MA", "3 Seasons", "Crime TV Shows, Docuseries, International TV Shows, TV Dramas",
        "DCP Vartika Chaturvedi tackles a sophisticated cyber-trafficking ring spanning northern states and international jurisdictions."
    ],
    [
        "s131", "TV Show", "Rana Naidu: Season 2", "Karan Anshuman, Suparn Verma", "Venkatesh Daggubati, Rana Daggubati, Surveen Chawla, Arjun Rampal", "India",
        "August 20, 2026", 2026, "TV-MA", "2 Seasons", "Action & Adventure, Crime TV Shows, International TV Shows, TV Dramas",
        "Rana and his father Naga form an uneasy alliance when international cartels expand their grip over southern film entertainment industries."
    ]
]

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"Generated {len(rows)} properly quoted records into {csv_file}")

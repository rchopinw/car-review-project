from web_core import *
from lda_core import *
from sa_core import *
from matplotlib import pyplot as plt
import pandas as pd

# Data Scrapping
core = WEB()
car_brand = core.get_car_brand()
car_brand_model = core.get_car_model(brand_info=car_brand)
car_review = core.get_car_review(brand_model_info=car_brand_model)

# DataFrame Formulating
df = []
rating_details = ['id', 'title', 'body', 'reliability', 'practicality', 'runningCost', 'howItDrives',
                  'overallRating', 'reviewDate', 'thumbsUpCount', 'thumbsDownCount', 'displayName',
                  'vehicleName']
for brand, brand_id in car_review:
    for model, model_id in car_review[(brand, brand_id)]:
        if not car_review[(brand, brand_id)][(model, model_id)]:
            df.append([brand, brand_id, model, model_id, None, None] + [None for _ in range(13)])
            continue
        for gen, gen_id in car_review[(brand, brand_id)][(model, model_id)]:
            print('Executing brand: {}, model: {}, generation: {}'.format(brand, model, gen))
            if not car_review[(brand, brand_id)][(model, model_id)][(gen, gen_id)]:
                df.append([brand, brand_id, model, model_id, gen, gen_id] + [None for _ in range(13)])
                continue
            for d in car_review[(brand, brand_id)][(model, model_id)][(gen, gen_id)]:
                df.append([brand, brand_id, model, model_id, gen, gen_id] + [d.get(x) for x in rating_details])
df = pd.DataFrame(df, columns=['brand', 'brand_id', 'model', 'model_id', 'generation', 'generation_id'] + rating_details)

# Sentiment Analysis model implementation
stop_words = load_stopwords()
df['unique_id'] = range(0, df.shape[0])
df['sentiment_score_bmodel'] = df['body'].apply(lambda x: sa_blob(x) if isinstance(x, str) else None)
df.to_csv('car_sa_review.csv', encoding='utf_8_sig', index=False)

# Generating Box plot differentiated by feature 'overallRating'
df_clean = df.dropna(subset=['sentiment_score_bmodel', 'overallRating'])
d = pd.DataFrame(dict(zip([x[0] for x in df_clean.groupby('overallRating')],
                          [pd.Series(x[1]['sentiment_score_bmodel'].tolist()) for x in df_clean.groupby('overallRating')])))
d.boxplot()
plt.ylabel('Sentiment Score (Ranging from -1 to 1)')
plt.xlabel('Overall Rating Score')
plt.savefig('./fig_output/Sentiment Score')
plt.show()
plt.close()

# LDA model
NUM_TOPICS = 30
raw_text = df.dropna(subset=['body'])['body'].tolist()
lda = LDAr(raw_text=raw_text,
           stop_words=sw,
           num_topics=NUM_TOPICS)
topics = lda.gen_topics()
terms = lda.gen_terms()
terms = sorted(terms, key=lambda x: x[2])

for tpi in range(NUM_TOPICS):
    t_df = pd.DataFrame(terms[tpi], columns=['Word', 'Idx', 'Portion'])
    plt.barh(y=t_df['Word'], width=t_df['Portion'])
    plt.ylabel('Topic Word Term')
    plt.xlabel('Portion')
    plt.title('Topic Term Distribution for Topic {}'.format(tpi))
    plt.savefig('./fig_output/Topic Term Distribution for Topic {}'.format(tpi))
    plt.show()
    plt.close()

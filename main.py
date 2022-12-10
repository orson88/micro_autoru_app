import pandas as pd
import streamlit as st
import plotly_express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from regress_analysis import bhp_growth
from data_process import main_processor
from dwn import get_csv, get_pickle
st.set_page_config(layout='wide',
                   initial_sidebar_state = 'collapsed')


def main():

    #intended way to work
    # try:
    #     df = pd.read_csv('auto_data.csv')
    # except:
    #     main_processor()
    #     df = pd.read_csv('auto_data.csv')
    #
    #the working way (thx to auto.ru and my laziness that i didnt use selenium in the first place)
    get_csv()
    tab1, tab2, tab3 = st.tabs(["Общая статистика", "Мониторинг моделей", "Рекомендации"])

    with tab1:
        st.header('Здесь можно ознакомиться с общей статистикой по машинам')

        con1 = st.container()
        with con1:
            m1, m2, m3 = st.columns(3)
            m1.metric("Всего объявлений", len(df))
            m2.metric("Новых объявлений", len(df[df['year'] >= 2021]))
            m3.metric("Уникальных машин", len(df['model_name'].unique()))

            col1, col2 = st.columns(2)
            with col1:
                fig1 = go.Figure(go.Bar(
                    x=df['model_name'].value_counts()[:10].values,
                    y=df['model_name'].value_counts()[:10].index,
                    orientation='h'
                ), {'title':'Самые популярные модели'})
                st.plotly_chart(fig1)

                fig2 = px.pie(df['gear_type'].value_counts().reset_index(),
                              values = 'gear_type', names = 'index', title='Распределение по приводам')
                st.plotly_chart(fig2)
            with col2:
                hist_data = []
                group_labels = []

                for bod in df['gear_type'].unique():
                    hist_data.append(list(df[df['gear_type'] == bod]['price'].values))
                    group_labels.append(bod)

                fig3 = ff.create_distplot(hist_data, group_labels, bin_size=1000000)
                fig3.update_layout({'title':'Распределение цен'})
                st.plotly_chart(fig3)
                df_for_fig4 = df.groupby('body_type').agg({'saleId':'count',
                                                           'price':'mean'}).reset_index()

                fig4 = px.scatter(df_for_fig4,
                                 x = 'body_type',
                                 y= 'saleId',
                                  size='price'
                                 )
                st.plotly_chart(fig4)








    with tab2:
        st.header('Просматривай конкретные модели тут!')
        st.text('Тыкай стрелочку в верхнем левом углу для настройки фильтров')
        xf = df
        with st.sidebar:
                st.header('Фильтры для мониторинга моделей')
                selected_model = st.sidebar.selectbox('Модель',
                                                     tuple(
                                                         xf['model_name'].unique()
                                                     )+(None,))
                xf = xf[xf['model_name'] == selected_model]

                selected_year = st.sidebar.selectbox('Год выпуска',
                                                     tuple(
                                                         sorted(xf['year'].unique())
                                                     )+(None,))
                xf = xf[xf['year'] == selected_year]


                selected_body_type = st.sidebar.selectbox('Кузов',
                                                     tuple(
                                                         xf['body_type'].unique()
                                                     )+(None,))
                xf = xf[xf['body_type'] == selected_body_type]

        st.dataframe(xf)


    with tab3:
        st.header('Хватит искать по брендам! Собери себе монстра')

        col1, col2 = st.columns(2)

        with col1:
            bhp = st.slider('Лошадки (л.с.)',
                            min_value=float(df['horsepower'].min()),
                            max_value=float(df['horsepower'].max()))

        with col2:
            korobka = st.multiselect('Коробочка', df['transmission'].unique(),
                                     default = ['MECHANICAL'])

        recdf = df[
                (df['horsepower'] < bhp * 1.2) & (df['horsepower'] > bhp * 0.8)
                & (df['transmission'].isin(korobka))
                ]
        recdf['rec'] = abs(recdf['horsepower'] - bhp)
        recdf.sort_values(by='rec', inplace = True)
        st.text('Средний ценник для каждой коробки')
        st.dataframe(recdf.groupby(['transmission'])['price'].mean().apply(lambda x: round(x)))
        st.text('Рекомендованные машины')
        st.dataframe(recdf.head(5))
        try:
            st.text(f"Каждые 10 новых лошадей стоят примерно {bhp_growth(bhp)}")
            st.text(f"Пока готовь {round(recdf.price.quantile(0.3)) / 1000000} млн. рупий")
        except:
            st.text(f"Нет такой машины...")

if __name__ == "__main__":
    main()
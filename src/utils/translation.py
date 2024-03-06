"""Functions used to translate query engine outputs"""

import pandas as pd
from deep_translator import GoogleTranslator


def get_list_languages():
    return GoogleTranslator().get_supported_languages()


def translator(
        text: str, translator_function,
        target: str = 'en', source: str = 'auto') -> str:
    if str(text) == 'nan':
        return ''
    elif len(text) <= 5000:
        return translator_function.translate(text=text)
    else:
        N = len(text) // 5000
        output = ''
        for k in range(N):
            input_plus = text[5000 * N: 5000 * (N + 1)]
            output += translator_function.translate(text=input_plus)
        output += translator_function.translate(text=text[5000 * (N + 1):])
        return output


def query_to_french(query):
    return GoogleTranslator(source='auto', target='french').translate(
        text=query)


def lead_text_translator(
        df: pd.DataFrame,
        column_names: list([str]) = ['Chapeau', 'Description'],
        target: str = 'en', source: str = 'auto') -> pd.DataFrame:
    if target == source:
        return df
    else:
        translator_function = GoogleTranslator(source=source, target=target)
        df_translated = df.copy()
        for column_name in column_names:
            translated = df.loc[:, column_name].apply(
                translator, args=(translator_function, target, source))
            df_translated[column_name] = translated
        return df_translated

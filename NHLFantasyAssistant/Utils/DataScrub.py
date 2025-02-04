import re
class DataScrub:
    def clean_data(df):
        if 'name' in df.columns:
            df['name'] = df['name'].apply(DataScrub.clean_name)
        return df

    def clean_name(name):
        cleaned_name = str(name)
        cleaned_name = re.sub(r'-', '/', cleaned_name)
        cleaned_name = re.sub(r'\b(Mc)([a-z])', lambda m: m.group(1) + m.group(2).upper(), cleaned_name)
        cleaned_name = re.sub(r'Aston/Reese', 'Aston-Reese', cleaned_name)
        cleaned_name = re.sub(r'Sttzle', 'Stutzle', cleaned_name)
        cleaned_name = re.sub(r'Lafrenire', 'Lafreniere', cleaned_name)

        return cleaned_name

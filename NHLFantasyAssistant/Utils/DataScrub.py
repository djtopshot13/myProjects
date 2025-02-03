import re
class DataScrub:
    def clean_data(self, df):
        if 'name' in df.columns:
            df['name'] = df['name'].apply(self.clean_name)
        return df

    def clean_name(self, name):
        cleaned_name = re.sub(r'-', '/', str(name))
        cleaned_name = re.sub(r'\b(Mc)([a-z])', lambda m: m.group(1) + m.group(2).upper(), name)
        cleaned_name = re.sub(r'Aston/Reese', 'Aston-Reese', name)

        return cleaned_name
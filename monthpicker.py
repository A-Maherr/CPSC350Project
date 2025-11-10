
from streamlit_date_picker import date_picker, PickerType

selected_month = date_picker(
            picker_type=PickerType.month,
            value=datetime.now(),
            key="month_picker"
            ) 
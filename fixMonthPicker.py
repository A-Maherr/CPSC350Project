import streamlit as st

class FixStreamlitDatePicker(object):
    def __init__(self):
        pass
    def patch_modules_streamlit_date_picker(self, name: str, file: str, old_code: str, new_code: str):
        import streamlit_date_picker
        import os
        import re

        relative_file_path = file
        library_root = list(streamlit_date_picker.__path__)[0]
        file_path = os.path.join(library_root, relative_file_path)

        # Replacement logic
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

        is_changed = False
        try:
            # Match the target class code block
            if name=='px':
                class_pattern = r"class px extends ua(.*?)this\.setComponentValue\(\)"
            elif name=='hx':
                class_pattern = r"class hx extends ua(.*?)const t=this\.props\.args\.refresh_buttons"
            match = re.search(class_pattern, content, re.DOTALL)
            old_class_body = match.group(1)
            new_class_body = old_class_body.replace(old_code, new_code)
            print(old_class_body)
            print(new_class_body)
            # Replace old code with new code
            updated_content = content.replace(old_class_body, new_class_body)
            is_changed = True
        except Exception as e:
            print(e)

        if is_changed:
            # Write back to file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(updated_content)
            import importlib
            importlib.reload(streamlit_date_picker)

        return True

    # Fix for streamlit_date_picker
    def patch_streamlit_date_picker(self):
        if st.button(label='Start fixing streamlit_date_picker package', type='primary'):
            # Fix for 1.44.0 default display height
            # Single selection fix
            self.patch_modules_streamlit_date_picker(
                name='px', 
                file=r'frontend/build/static/js/main.78ff4c09.js',
                old_code='this._onOpenChange=e=>{sa.setFrameHeight(450),super.componentDidUpdate()}',
                new_code='this._onOpenChange=(e=>{sa.setFrameHeight(450);const t=document.getElementById("root");e?(this.resizeObserver&&(this.resizeObserver.disconnect(),this.resizeObserver=null),this.mutationObserver&&(this.mutationObserver.disconnect(),this.mutationObserver=null),this.mutationObserver=new MutationObserver((e,s)=>{const r=document.querySelector(".ant-picker-dropdown");r&&(this.resizeObserver=new ResizeObserver(e=>{for(const s of e){const e=s.contentRect.height;t.style.height=e+50+"px"}}),this.resizeObserver.observe(r),s.disconnect(),this.mutationObserver=null)}),this.mutationObserver.observe(document.body,{childList:!0,subtree:!0})):(t.style.height="",this.resizeObserver&&(this.resizeObserver.disconnect(),this.resizeObserver=null),this.mutationObserver&&(this.mutationObserver.disconnect(),this.mutationObserver=null)),super.componentDidUpdate()})'
                )
            # Multi selection fix
            self.patch_modules_streamlit_date_picker(
                name='hx', 
                file=r'frontend/build/static/js/main.78ff4c09.js',
                old_code='this._onOpenChange=e=>{sa.setFrameHeight(450),super.componentDidUpdate()}',
                new_code='this._onOpenChange=(e=>{sa.setFrameHeight(460);const t=document.getElementById("root");e?(this.resizeObserver&&(this.resizeObserver.disconnect(),this.resizeObserver=null),this.mutationObserver&&(this.mutationObserver.disconnect(),this.mutationObserver=null),this.mutationObserver=new MutationObserver((e,s)=>{const r=document.querySelector(".ant-picker-dropdown");r&&(this.resizeObserver=new ResizeObserver(e=>{for(const s of e){const e=s.contentRect.height;t.style.height=e+70+"px"}}),this.resizeObserver.observe(r),s.disconnect(),this.mutationObserver=null)}),this.mutationObserver.observe(document.body,{childList:!0,subtree:!0})):(t.style.height="",this.resizeObserver&&(this.resizeObserver.disconnect(),this.resizeObserver=null),this.mutationObserver&&(this.mutationObserver.disconnect(),this.mutationObserver=null)),super.componentDidUpdate()})'
                )
            # Multi selection flicker fix
            self.patch_modules_streamlit_date_picker(
                name='hx', 
                file=r'frontend/build/static/js/main.78ff4c09.js',
                old_code='style:{height:"60px",display:"flex",alignItems:"center"}',
                new_code='style:{height:"60px",alignItems:"center"}'
                )
            st.success('Fix completed', icon='✅')

if __name__ == "__main__":  
    tabs = st.tabs(tabs=[':material/schedule: streamlit_date_picker'])
    with tabs[0]:
        st.markdown(
            body='''
                ### Fix details
                - Since Streamlit 1.44.0, the third-party library `streamlit_date_picker` has a bug where the date/time picker component cannot be displayed correctly
                - Fixes for version 1.44.0 support both single date/time picker and date/time range picker
            ''',
            unsafe_allow_html=False
        )
        fsac = FixStreamlitDatePicker()
        fsac.patch_streamlit_date_picker()
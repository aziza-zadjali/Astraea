
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
/
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
m
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
n
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
t
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
/
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
d
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
a
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
t
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
a
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
/
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
a
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
p
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
p
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
_
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
c
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
o
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
r
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
r
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
e
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
c
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
t
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
e
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
d
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
_
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
1
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
8
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
.
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
p
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")
y
def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")

    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    submit_button = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
    
    if submit_button:
        if query:
            process_query(query, summary_type, context=None, lang_code=lang_code)
        else:
            st.warning("Please enter a query before submitting.")

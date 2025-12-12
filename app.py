import streamlit as st
import os
import pandas as pd
from io import BytesIO
from extractor import extract_data
from collector import collect_data

# Page configuration
st.set_page_config(
    page_title="Amazon Product Scraper",
    page_icon="🛒",
    layout="wide"
)

# Create data folder if it doesn't exist
DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Title
st.title("🛒 Amazon Product Scraper")
st.markdown("Extract product data from Amazon and download as Excel/CSV")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Scraping Configuration")
    keyword = st.text_input("Product Keyword", value="Mobile_Phones", 
                           help="Enter the product category or keyword to search")
    max_pages = st.number_input("Number of Pages", min_value=1, max_value=20, value=5,
                                help="Number of Amazon pages to scrape")
    
    st.divider()
    
    st.header("📋 Data to Extract")
    extract_name = st.checkbox("Product Name", value=True)
    extract_price = st.checkbox("Price", value=True)
    extract_rating = st.checkbox("Rating", value=True)
    extract_link = st.checkbox("Product Link", value=True)
    extract_img = st.checkbox("Image Link", value=True)
    
    st.divider()
    
    st.info("💡 **Tip:** Start with fewer pages to test, then increase for full extraction.")

# Main content ar
tab1, tab2 = st.tabs(["🔍 Scraper", "📊 Data Viewer"])

with tab1:
    # Main buttons
    col1, col2 = st.columns(2)
    
    with col1:
        scrape_button = st.button("🔍 Scrape & Extract", type="primary", use_container_width=True)
    
    with col2:
        extract_button = st.button("📊 Extract from Existing Files", use_container_width=True)
    
    st.divider()
    
    # Scrape and Extract
    if scrape_button:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Collect data
            status_text.text("🔄 Step 1/2: Collecting data from Amazon...")
            with st.spinner("Scraping Amazon pages..."):
                files_saved = collect_data(keyword, max_pages, DATA_FOLDER)
            progress_bar.progress(50)
            st.success(f"✅ Collected {files_saved} product files")
            
            # Step 2: Extract data
            status_text.text("🔄 Step 2/2: Extracting product information...")
            with st.spinner("Parsing HTML and extracting data..."):
                df, stats = extract_data(
                    DATA_FOLDER, 
                    is_name=extract_name,
                    is_price=extract_price,
                    is_link=extract_link,
                    is_rating=extract_rating,
                    is_img=extract_img
                )
            progress_bar.progress(100)
            status_text.text("✅ Extraction complete!")
            
            # Store in session state
            st.session_state.df = df
            st.session_state.stats = stats
            st.session_state.keyword = keyword
            
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Error occurred: {str(e)}")
            with st.expander("🐛 View Error Details"):
                import traceback
                st.code(traceback.format_exc())
    
    # Extract Only
    if extract_button:
        with st.spinner("📊 Extracting data from existing files..."):
            try:
                df, stats = extract_data(
                    DATA_FOLDER,
                    is_name=extract_name,
                    is_price=extract_price,
                    is_link=extract_link,
                    is_rating=extract_rating,
                    is_img=extract_img
                )
                
                st.session_state.df = df
                st.session_state.stats = stats
                st.session_state.keyword = keyword
                st.success(f"✅ Extracted {len(df)} products from {stats['total_files']} files")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                with st.expander("🐛 View Error Details"):
                    import traceback
                    st.code(traceback.format_exc())

with tab2:
    # Display results if data exists
    if 'df' in st.session_state and 'stats' in st.session_state:
        df = st.session_state.df
        stats = st.session_state.stats
        keyword = st.session_state.get('keyword', 'products')
        
        # Display statistics
        # st.subheader("📊 Extraction Statistics")
        
        # col1, col2, col3, col4, col5 = st.columns(5)
        
        # with col1:
        #     st.metric("Total Files", stats['total_files'])
        # with col2:
        #     st.metric("Total Products", len(df))
        # with col3:
        #     st.metric("Complete Records", stats['complete_records'])
        # with col4:
        #     missing_total = max(stats['missing_names'], stats['missing_prices'],  
        #                    stats['missing_ratings'], stats['missing_links'],
        #                    stats['missing_images'])
        #     st.metric("Missing Data Points", missing_total)
        # with col5:
        #     st.metric("Errors", stats['errors'])
        
        # Detailed stats in expander
        # with st.expander("📈 View Detailed Statistics"):
        #     col1, col2 = st.columns(2)
        #     with col1:
        #         st.write("**Missing Data Breakdown:**")
        #         st.write(f"• Missing Names: {stats['missing_names']}")
        #         st.write(f"• Missing Prices: {stats['missing_prices']}")
        #         st.write(f"• Missing Ratings: {stats['missing_ratings']}")
        #     with col2:
        #         st.write("**Quality Metrics:**")
        #         st.write(f"• Missing Links: {stats['missing_links']}")
        #         st.write(f"• Missing Images: {stats['missing_images']}")
        #         st.write(f"• Processing Errors: {stats['errors']}")
        #         completion_rate = (stats['complete_records'] / len(df) * 100) if len(df) > 0 else 0
        #         st.write(f"• Completion Rate: {completion_rate:.1f}%")
        
        st.divider()
        
        # Download buttons
        st.subheader("📥 Download Extracted Data")
        
        col1, col2, col3 = st.columns(3)
        
        # Excel Download
        with col1:
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Products')
                
                # Add statistics sheet
                stats_df = pd.DataFrame([stats])
                stats_df.to_excel(writer, index=False, sheet_name='Statistics')
            
            buffer.seek(0)
            
            st.download_button(
                label="📊 Download Excel (.xlsx)",
                data=buffer,
                file_name=f"{keyword}_products.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        # CSV Download
        with col2:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📄 Download CSV",
                data=csv,
                file_name=f"{keyword}_products.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # JSON Download
        with col3:
            json_str = df.to_json(orient='records', indent=2)
            st.download_button(
                label="📋 Download JSON",
                data=json_str,
                file_name=f"{keyword}_products.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.divider()
        
        # Display data preview
        st.subheader("👀 Data Preview & Filtering")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            show_complete = True
        with col2:
            search_term = st.text_input("🔍 Search products", "", placeholder="Enter product name...")
        with col3:
            show_rows = st.selectbox("Rows to display", [10, 25, 50, 100, "All"], index=1)
        
        # Apply filters
        filtered_df = df.copy()
        
        if show_complete:
            filtered_df = filtered_df[
                (filtered_df['Product Name'] != "N/A") &
                (filtered_df['Price'] != "N/A") &
                (filtered_df['Rating'] != "N/A") &
                (filtered_df['Product URL'] != "N/A") &
                (filtered_df['Image URL'] != "N/A")
            ]
        
        if search_term:
            filtered_df = filtered_df[
                filtered_df['Product Name'].str.contains(search_term, case=False, na=False)
            ]
        
        st.info(f"📊 Showing {len(filtered_df)} of {len(df)} products")
        
        # Display dataframe
        if show_rows != "All":
            filtered_df = filtered_df.head(int(show_rows))
        
        st.dataframe(
            filtered_df,
            use_container_width=True,
            column_config={
                "Product URL": st.column_config.LinkColumn("🔗 Product Link"),
                "Image URL": st.column_config.LinkColumn("🖼️ Image Link"),
                "Price": st.column_config.TextColumn("💰 Price"),
                "Rating": st.column_config.TextColumn("⭐ Rating")
            },
            height=500
        )
    
    else:
        st.info("👈 No data available. Please scrape or extract data from the 'Scraper' tab first.")
        st.markdown("""
        ### How to use:
        1. Configure scraping settings in the sidebar
        2. Click **"Scrape & Extract"** to collect new data
        3. Or click **"Extract from Existing Files"** to process saved HTML files
        4. View and download the extracted data here
        """)

# Footer
st.divider()
st.caption("🛒 Amazon Product Scraper | Built with Streamlit")
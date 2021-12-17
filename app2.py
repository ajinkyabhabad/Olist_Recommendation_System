import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import boto3 
from io import StringIO
import os
import json


def main():
	
	def Recommendations_ALS(Customer_id):
		#Olist_db_ = Olist_db_[Olist_db_.Customer_ID < 3600]
		fave_prod = Olist_db_.groupby(['CUSTOMER_ID']).max()['PRODUCT_ID'].to_frame()
		fave_prod = fave_prod.reset_index()
		
		#prd_id = get_prod_id(Customer_id)
		prd_id = fave_prod[fave_prod.CUSTOMER_ID == Customer_id]['PRODUCT_ID']
		Product_id = prd_id.iloc[0]
		product_names = list(X.index)
		product_ID_Idx = product_names.index(Product_id)
		
		correlation_product_ID = correlation_matrix[product_ID_Idx]
		
		Recommend = list(X.index[correlation_product_ID > 0.70])
		# Removes the item already bought by the customer
		Recommend.remove(Product_id) 
		
		## Getting Product names froom prediction 

		predictions = pd.DataFrame(Recommend[:20])
		predictions.columns = ['Product_ID']

		predictions['Product_ID'] = predictions.Product_ID.apply(lambda x : Olist_db_[Olist_db_.PRODUCT_ID == x]['PRODUCT_ID'].unique()[0])
		Recommendations = predictions[:10]
		SA = Olist_db[['PRODUCT_ID','REVIEW_SCORE','PAYMENT_VALUE']]
		Recommendations = pd.merge(Recommendations,SA, right_on ='PRODUCT_ID',left_on = 'Product_ID', how = 'inner' )
		Recommendations = Recommendations[['PRODUCT_ID','REVIEW_SCORE','PAYMENT_VALUE']]
		Recommendations = Recommendations.rename(columns = {'PAYMENT_VALUE':'PRODUCT_PRICE'})
		Recommendations = Recommendations.groupby('PRODUCT_ID').mean()
		Recommendations = Recommendations.reset_index()
		return Recommendations

	def Recommendations_ALS_Reg(Customer_id):
		fave_prod = Olist_Reg_db_.groupby(['CUSTOMER_ID']).max()['PRODUCT_ID'].to_frame()
		fave_prod = fave_prod.reset_index()
		prd_id = fave_prod[fave_prod.CUSTOMER_ID == Customer_id]['PRODUCT_ID']
		Product_id = prd_id.iloc[0]
		product_names = list(X_Reg.index)
		product_ID_Idx = product_names.index(Product_id)
		correlation_product_ID = correlation_matrix_Reg[product_ID_Idx]
		Recommend = list(X_Reg.index[correlation_product_ID > 0.70])
		Recommend.remove(Product_id)
		predictions = pd.DataFrame(Recommend[:20])
		predictions.columns = ['Product_ID']
		predictions['Product_ID'] = predictions.Product_ID.apply(lambda x : Olist_Reg_db_[Olist_Reg_db_.PRODUCT_ID == x]['PRODUCT_ID'].unique()[0])
		Recommendations = predictions[:10]
		A_S = Olist_Reg_db[['PRODUCT_ID','REVIEW_SCORE','PAYMENT_VALUE']]
		Recommendations = pd.merge(Recommendations,A_S, right_on ='PRODUCT_ID',left_on = 'Product_ID', how = 'inner' )
		Recommendations = Recommendations[['PRODUCT_ID','REVIEW_SCORE','PAYMENT_VALUE']]
		Recommendations = Recommendations.rename(columns = {'PAYMENT_VALUE':'PRODUCT_PRICE'})
		Recommendations = Recommendations.groupby('PRODUCT_ID').mean()
		Recommendations = Recommendations.reset_index()
		return Recommendations
	
	Olist_db = pd.read_csv('/home/sanket/streamlit/best.csv')
	Olist_db_ = pd.read_csv('/home/sanket/streamlit/Olist_db_ALS.csv')
	X = pd.read_csv('/home/sanket/streamlit/X_ALS.csv', index_col=0)
	with open('/home/sanket/streamlit/correlation_matrix_ALS.txt') as f:
		correlation_matrix = json.load(f)
	correlation_matrix = np.array(correlation_matrix)

	Olist_Reg_db = pd.read_csv('/home/sanket/streamlit/Regular.csv')
	with open('/home/sanket/streamlit/correlation_matrix_ALS_Reg.txt') as g:
		correlation_matrix_Reg = json.load(g)
	Olist_Reg_db_ = pd.read_csv('/home/sanket/streamlit/Olist_Reg_db_ALS.csv')
	X_Reg = pd.read_csv('/home/sanket/streamlit/X_ALS_Reg.csv', index_col=0)
	correlation_matrix_Reg = np.array(correlation_matrix_Reg)
	

    
	#os.chdir('/home/sanket/streamlit/Superstore_Heroku')

	page_bg_img = '''
	<style>
	body {
	background-image: url("https://s3.envato.com/files/312214659/239_1R3A9317.jpg");
	background-size: cover;
	}
	</style>
	'''

	st.markdown(
    """
	<style>
	.reportview-container .markdown-text-container {
    font-family: monospace;
	}
	.sidebar .sidebar-content {
    background-image: linear-gradient(#f07470, #f1959b, #f6bdc0);
    color: white;
	}
	.Widget>label {
    color: black;
    font-family: monospace;
    font-size:15px;
	}
	</style>
	""",unsafe_allow_html=True)


	st.markdown(page_bg_img, unsafe_allow_html=True)

	pass_data = pd.read_csv('Passwords.csv')
	popular= pd.read_csv('df_popular.csv')

	pass_data['Customer_ID']=pass_data['Customer_ID'].astype(str)

	menu = ["HomePage","Login", "New Customer"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "HomePage":
		bgcolor="#010000"
		fontcolor = "#FFFFFF"


		html_temp = """
		<div style="background-color:{};padding:10px">
		<h1 style="color:{};text-align:center;">The Olist Recommendation System</h1>
		</div>
		"""
		st.markdown(html_temp.format(bgcolor,fontcolor),unsafe_allow_html=True)

		html_temp1 = """
		<div> <h1 style='text-align: center; color: red;'>Some title</h1> </div>
		"""

		#st.markdown("<p style='text-align: center; color: red;'>Some title</p>", unsafe_allow_html=True)

		st.markdown('<style>h1 { font-size: 72px;background: -webkit-linear-gradient(#FFFF, #00FF);-webkit-background-clip: text;-webkit-text-fill-color: transparent;}</style>', unsafe_allow_html=True)
		
		#st.title("The Olist Recommendation System")
		st.markdown('<style>h2 { font-size: 72px;background: -webkit-linear-gradient(#FFFF, #00FF);-webkit-background-clip: text;-webkit-text-fill-color: transparent;}</style>', unsafe_allow_html=True)
		st.markdown(" Here are some personalised products for you!")
		st.image('back.jpg',use_column_width=200)
		#st.header("What are looking for today?")
		st.markdown("Login to see the recommendations we have for you!")
		st.markdown("If you are a New Customer, Check out our Recommendations for you as well!!")

	elif choice == "Login":		
		#users = pass_data['Customer_ID'].unique().tolist()
		username = st.sidebar.text_input("User Name")
		username = str(username)
		password = st.sidebar.text_input("Password",type = 'password')
		x=pass_data[pass_data['Customer_ID']==username]
		lbtn=st.sidebar.button("Login")
 
		if lbtn:
			if x.empty:
				st.warning("Invalid User Name/Password")

			elif(username==""):
				st.warning("User Name cannot be empty")
			elif(password==""):
				st.warning("Password cannot be empty")
			elif((x.iloc[0].Customer_ID==username) & (x.iloc[0].Password==password)):
				st.success("Logged in as {}".format(username))
				#st.subheader("Recommendations for you:")
				mask = np.column_stack([Olist_db['CUSTOMER_ID'].str.contains(username, na=False) for CUSTOMER_ID in Olist_db])
				mask_Reg = np.column_stack([Olist_Reg_db['CUSTOMER_ID'].str.contains(username, na=False) for CUSTOMER_ID in Olist_Reg_db])
				if len(Olist_db.loc[mask.any(axis=1)]) > 0:
					st.subheader("Recommendations for our best Customers:")
				#if Olist_db[Olist_db['CUSTOMER_ID'].str.contains(username)]:
					A = Recommendations_ALS(username)
					st.dataframe(A)
				elif len(Olist_Reg_db.loc[mask_Reg.any(axis=1)]) > 0:
					st.subheader("Recommendations for our regular Customers:")
					B = Recommendations_ALS_Reg(username)
					st.dataframe(B)
				else:
					st.subheader("Recommendations for you")
					sb = popular[['PRODUCT_ID','REVIEW_SCORE','Product_Price']]
					sb = sb.sort_values(by='REVIEW_SCORE',ascending=False)
					sb = sb.rename(columns={'Product_Price':'PRODUCT_PRICE'})
					sb = sb.head(10)
					st.dataframe(sb.reset_index())

				#user_top_k = data[data['Customer_ID']==int(username)]
				#st.dataframe(user_top_k[['ProductID','ProductName','Category','Sub-Category']].head(10))
			elif((x.iloc[0].Customer_ID!=username) | (x.iloc[0].Password!=password)):
				st.warning("Invalid User Name/Password")
			
	elif choice == "New Customer":
		st.subheader("Recommendations for you")
		s = popular[['PRODUCT_ID','REVIEW_SCORE','Product_Price']]
		s = s.rename(columns={'Product_Price':'PRODUCT_PRICE'})
		sort =st.selectbox('Sort By',['Popularity','Price - Low to High','Price - High to Low'])
		if(sort=='Price - Low to High'):
			st.dataframe(s.sort_values(by='PRODUCT_PRICE',ascending=True)[['PRODUCT_ID','REVIEW_SCORE','PRODUCT_PRICE']].reset_index().head(10))
		elif(sort=='Price - High to Low'):
			st.dataframe(s.sort_values(by='PRODUCT_PRICE',ascending=False)[['PRODUCT_ID','REVIEW_SCORE','PRODUCT_PRICE']].reset_index().head(10))	
		else:
			st.dataframe(s.sort_values(by='REVIEW_SCORE',ascending=False)[['PRODUCT_ID','REVIEW_SCORE','PRODUCT_PRICE']].reset_index().head(10))
				

if __name__ == '__main__':
	main()

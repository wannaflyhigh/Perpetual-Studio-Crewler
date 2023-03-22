import requests as req
import bs4

def simpleQuery(params={}, url=''):
	res = ''
	if (url != ''):
		res = req.get(url)
	else:
		postUrl = "http://www.lib.ntnu.edu.tw/holding/doQuickSearch.jsp"
		res = req.post(postUrl, params)
	table = bs4.BeautifulSoup(res.text,
							  features="html.parser").find_all('table')
	aTags = table[0].find_all('a')

	bookTypes = []

	for aTag in aTags:
		name = str(aTag.contents[0]).strip()
		href = 'http://www.lib.ntnu.edu.tw/holding/' + \
			str(aTag.get('href')).replace("¶", "&para")
		bookTypes.append({'name': name, 'href': href})

	pages = bs4.BeautifulSoup(res.text, features="html.parser").find_all(
		'div', {'class': 'jumppage'})[0].find_all('a')
	pageLinks = []
	for page in pages:
		name = str(page.contents[0]).strip()
		href = 'http://www.lib.ntnu.edu.tw/holding/' + \
			str(page.get('href')).replace("¶", "&para")
		pageLinks.append({'name': name, 'href': href})

	result = {'bookTypes': bookTypes, 'pageLinks': pageLinks}
	return result

def singleBookOrMulti(options):
	aS = options[0].find_all('a')
	for a in aS:
		if(a.contents[0] == '顯示MARC'):
			return 'single'
	return 'multi'

def findBook(url):
	res = req.get(url)
	options = bs4.BeautifulSoup(res.text,features="html.parser").find_all('div', {"class": "options"})
	print(singleBookOrMulti(options)=='single')
	if(singleBookOrMulti(options)=='single'):
		return singleBook(res.text)
	else:
		return multiBook(res.text)


def multiBook(text):
	books = []
	bookNameAndHrefs = bs4.BeautifulSoup(text,features="html.parser").find_all(
		'tr', {"valign": "top"})
	for index, bookNameAndHref in enumerate(bookNameAndHrefs):
		bookDetail = {}
		href = ''
		name = ''
		a = bookNameAndHref.find_all('a', href=True)
		i = 0
		if (a[0].contents[0] == '預約'):
			i = 1
		href = 'http://www.lib.ntnu.edu.tw/holding/' + \
			str(a[i].get('href')).replace("¶", "&para")
		name = a[i].find_all('span')[0].contents[0]
		books.append({'href': href, 'name': name})
	tables = bs4.BeautifulSoup(text,features="html.parser").find_all('table',
												  {'class': 'width100'})
	for index, table in enumerate(tables):
		bookDetails = []
		for i, td in enumerate(table.find_all('tr')[1].find_all('td')):
			if (i == 4):
				break
			detail = td.contents[0]
			if (i == 1 or i == 2):
				detail = td.find_all('a')[0].contents[0]
			bookDetails.append(detail)
		books[index]['detail'] = bookDetails
	return books

def singleBook(text):
	table = bs4.BeautifulSoup(text,features="html.parser").find_all('table',
												  {'class': 'collection_info'})[0]
	bookDetails = []
	for i, td in enumerate(table.find_all('tr')[1].find_all('td')):
		if (i == 4):
			break
		detail = td.contents[0]
		if (i == 1 or i == 2):
			detail = td.find_all('a')[0].contents[0]
		bookDetails.append(detail)
	return bookDetails

# def test():
# 	url = "http://www.lib.ntnu.edu.tw/holding/doQuickSearch.jsp?action=view&param=%2Fsearch*cht%3F%2Ft%7Bu6F14%7D%7Bu7B97%7D%7Bu6CD5%7D%2Ft%7B214852%7D%7B21502c%7D%7B21472a%7D%2F1%252C24%252C31%252CB%2Fexact%26FF%3Dt%7B214852%7D%7B21502c%7D%7B21472a%7D%261%252C4%252C"
# 	# url='http://www.lib.ntnu.edu.tw/holding/doQuickSearch.jsp?action=view&param=%2Fsearch*cht%3F%2Ft%257Bu6F14%257D%257Bu7B97%257D%257Bu6CD5%257D%2Ft%257B214852%257D%257B21502c%257D%257B21472a%257D%2F1%252C24%252C31%252CB%2Fframeset%26FF%3Dt%7B214852%7D%7B21502c%7D%7B21472a%7D%261%252C%252C4'
# 	a=findBook(url)
# 	print(a)

# test()
# Welcome to the Indeed Job Scraper!

This python program includes code which will retrieve the user's input, which asks for a job title and city location to search for. After receiving the input the program scrapes the proper url from Indeed, and presents the first 10 postings in a neat pandas data frame. The program then asks the user if they want to view the next page (Y/N), and will follow accordingly. 

Please note this project is not without its bugs... some job title / city pairings produce errors with the pandas data frame requiring specific array lengths. I've set the lengths to 10, though it still breaks from time to time.

Cheers!

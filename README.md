# Social Security Number Guesser

This project is currently still in development. The end goal is to develop a method to estimate Social Security Numbers given birthdate, time, and location. I am using SQLite to manage the data.

Birth Data is a collection of data about births, some from the SSA and some from other sources. 

SSN-Raw-Data is a collection of the Highest Known Group Number files from the SSA.

**Next Steps**

After some research into the Death Master File, I have found a set of the files and will be using that as a source for machine learning along with the other data I've collected.


**Some History on the SSN**

In *1935*, FDR signed the Social Security Act into law, creating the system for Social Security. <sup>1</sup>

On *Tuesday, November 24, 1936*, Social Security Numbers began to be distributed by post offices as the SSA did not have local branches yet. <sup>2</sup>

In *1972*, Social Security Numbers began to be assigned from the main office in Baltimore via the zip code of the letter receieved. Previously, SSNs were assigned based on what office people got their number from.<sup>3</sup>

In *1986*, major changes were made to the way employment and tax credits interacted with the SSN, requiring it for the dependent tax credit and allowing employers to use it for employment verification.<sup>4</sup>

In *1987*, the SSA began a program allowing children born in New Mexico to be automatically assigned SSNs at birth at a parent's request, and this was expanded nationally by *1989*.<sup>4</sup>

On *June 25, 2011*, the SSA began assigning SSNs randomly, removing the meaning of the area number and the group numbers, and assigning some numbers that had previously been unassigned.<sup>5</sup>

Sources:
1 - https://www.ssa.gov/history/briefhistory3.html
2 - https://www.ssa.gov/history/ssn/firstcard.html
3 - https://www.ssa.gov/history/ssn/geocard.html
4 - https://www.ssa.gov/history/ssn/ssnchron.html
5 - https://www.ssa.gov/employer/randomization.html

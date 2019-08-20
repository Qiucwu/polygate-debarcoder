# polygate-debarcoder
Takes cyTOF and polygon gates and outputs gated data with positive three tag barcodes
Originally intended for use in debarcoding data obtained from cyTOF using protein barcodes introduced in  <a href="https://www.sciencedirect.com/science/article/pii/S0092867418312340?via%3Dihub">Wroblewska et al. 2018</a>.

To install from source:
<blockquote>
<pre>git clone https://github.com/Qiucwu/polygate-debarcoder 
cd polygate_debarcoder
pip install -r requirements.txt </pre>
</blockquote>

Install dependencies using pip install
<blockquote>
<pre>pip install FlowCytometryTools
pip install fcswrite </pre>
</blockquote>


## Quick Start
Open terminal and navigate to path of the program. Run init.py file
<blockquote> 
  <pre> python init.py </pre> </blockquote>
<p> You will be prompted to provide the following input files: </p>
<ol>
  <li>Gate coordinate files placed into folder ('coordinates')(refer to list section below for coordinate file formatting)</li>
  <li>CyTOF FCS file placed into folder ('fcs_file')</li>
  <li>Folder name</li>
</ol>
<p> Outputs will be saved into folder ('Debarcoded Files'): </p>
<ol>
  <li>Individual debarcoded files</li>
  <li>Distribution of barcodes within cell population</li>
  <li>List of Missing Barcodes</li>
</ol>

## Gate Coordinate Requirement
The formating of the gate coordinates files is essential for running the program. Make sure that you have your gate coordinates file in an .xls file in the format dictacted below. An example gate coordinates file will be provided in the folder "coordinates"
Gates are currently obtained from flowjo by gating on (x) metal of interest and (y) NGFR(metal 149). You may change the metal on the y-axis that you are gating for, but be sure to change it in the gate functions.

<table> <tr> <th>Metal</th>	<th>Name</th>	<th>Statistic</th>	<th>#Cells</th>	<th>Gate Coordinates</th> </tr>
  <tr> <td> mass of metal </td>
    <td> name of tag </td>
    <td> % of cells positive for that metal </td>
    <td> absolute number of cells positive for that metal </td>
    <td> <b>quatrilateral</b> gate coordinates exported from flowjo/FCSexpress </td>
  </tr>
  </table>
 

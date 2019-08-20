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


<b>Quick Start</b>
<p>The program takes input files: </p>
<ol>
  <li>Gate coordinate files (refer to list section below for coordinate file formatting)</li>
  <li>CyTOF FCS file</li>
  <li>Folder name</li>
</ol>
<p> Outputs: </p>
<ol>
  <li>Individual debarcoded files</li>
  <li>Distribution of barcodes within cell population</li>
  <li>List of Missing Barcodes</li>
</ol>

Gate Coordinate file requirement:

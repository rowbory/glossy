<?xml version="1.0" encoding="UTF-8"?><!-- DWXMLSource="Lexicon.xml" -->
<!DOCTYPE xsl:stylesheet  [
	<!ENTITY nbsp   "&#160;">
	<!ENTITY copy   "&#169;">
	<!ENTITY reg    "&#174;">
	<!ENTITY trade  "&#8482;">
	<!ENTITY mdash  "&#8212;">
	<!ENTITY ldquo  "&#8220;">
	<!ENTITY rdquo  "&#8221;"> 
	<!ENTITY pound  "&#163;">
	<!ENTITY yen    "&#165;">
	<!ENTITY euro   "&#8364;">
]>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8" doctype-public="-//W3C//DTD XHTML 1.1//EN" doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"/>
<xsl:template match="/">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<title><xsl:value-of select="Lexicon/Language/text()"/> Lexicon</title>
<script type="text/javascript" src="jquery.1.5.1/jquery.min.js"></script>
<script type="text/javascript" src="jquery.tablesorter/jquery.tablesorter.js"></script>
<script type="text/javascript" src="jquery.tablesorter/jquery.metadata.js"></script> 
<link href="jquery.tablesorter/themes/blue/style.css" rel="stylesheet" type="text/css"></link>
<style type="text/css">
table.tablesorter {
	width: auto;
}

table.tablesorter tbody tr td {
	font-size: 16pt;
	font-family: "Charis SIL Compact", "Charis SIL", "Andika Basic", "Arial Unicode MS";	
}

table.tablesorter thead td { max-height: 44px; }

table.tablesorter thead input {
	left: 0px; position: relative;
}
table.tablesorter thead input {
	z-index: 10;
}

table.tablesorter thead .behind_search {
	z-index: 0; color: white; display: none;
}

table.tablesorter thead tr th, table.tablesorter thead input, table.tablesorter thead .behind_search {
	text-align: center;
	font-family: "Andika Basic", "Arial Unicode MS";
	font-size: 20pt;
}
table.tablesorter thead td { margin: auto; text-align: center; }
table.tablesorter thead input { width: 99%; opacity: 0.2; border: none; background: white; margin: auto; text-align: center; }
table.tablesorter thead input:hover, table.tablesorter thead input.active { opacity: 1; }
table.tablesorter, table.tablesorter tbody, table.tablesorter tbody tr td { border-spacing: 0px; }
table.tablesorter tr td { border: 0px white solid; border-bottom: 1px gray solid; }
.tablesorter td:hover { color: blue; text-decoration: underline; cursor: pointer; }
.highlight { color: red; background-color: #ff9; }
</style>
</head>

<body>

<table class="tablesorter"><thead><tr><td colspan="2"><input id="search_target" type="text" title="Type text here to search" /><!-- </td><td><input id="search_gloss" type="text"/>--></td></tr><tr><th title="Target"><xsl:value-of select="Lexicon/Language/text()"/>
</th><th>Gloss</th></tr></thead>
<tbody>
<xsl:for-each select="//Sense">
<tr><td><xsl:value-of select="../../Lexeme/@Form"/></td><td><xsl:value-of select="Gloss/text()"/></td></tr>
</xsl:for-each>
</tbody>
</table>

<script type="text/javascript">
$(function () {
	var myTextExtraction = function(node) {  
		// extract data from markup and return it  
		return $(node).text();
	} 
	$(".tablesorter").tablesorter({textExtraction: myTextExtraction, sortList: [[0,0],[1,0]]});
	
	$("input").focus( function () { $(this).addClass("active"); } )
				.blur( function () { $(this).removeClass("active"); } )
				.keyup( function (e) {
					search_text = $(this).val();
					if (search_text.length==0) {
						// display all, when we clear the search box
						unsearch();
					} else if (search_text.length==1) {
						// type a single char and find all the TARGET language words BEGINNING with that char
						$(".tablesorter tbody tr").hide().each( function () {
							if ($(this).children("td").text().indexOf(search_text)==0) {
								$(this).show();
							}
						});
					} else {
						// normally, we search every row and every cell in each row for some text we want
						// then highlight the search text found with a span that gets deleted when we unsearch
						$(".tablesorter tbody tr").hide().each( function () {
							//if ($(this).children("td").text().indexOf(search_text)!=-1) {
								//$(this).show();
								tr = $(this);
								$(this).children("td").each( function () {
									// OLD WAY $(this).html(highlight_text($(this).text(),search_text));	
									this_cell = $(this).text();
									left_pos = this_cell.search(search_text);
									if (left_pos!=-1) {
										tr.show();
									}
								});
							//}
						});
					}
				});
	$(".tablesorter td").click( function () {
		this_word = $(this).text();
		if ($("#search_target").val()==this_word) {
			unsearch();
			$("#search_target").val("").focus();
		} else {
			$("#search_target").val(this_word).keyup().focus();
		}
	});
});

function unsearch() {
	$(".tablesorter tr").show();
	$(".highlight").removeClass("highlight");
}

$(function () {
	$("#search_target").focus();
});
</script>
</body>
</html>

</xsl:template>
</xsl:stylesheet>
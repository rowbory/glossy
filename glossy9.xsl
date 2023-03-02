<?xml version="1.0" encoding="UTF-8"?>
<!-- Glossy 1.9 david@rowbory.co.uk
Changes:
1.9: for Paratext 9
Lexicon
	Entries
		item	*
			Lexeme	@Form
			Entry
				Sense	*
					Gloss
				Sense	*
					Gloss

1.6
	Sort and search equivalents hard-coded as a trial. (ə=a underline, ɨ=i underline)
1.5.1 June 2014
	A bit more finesse with the sort-from-end option, more documentation in files and robustness of the batch file
1.5	June 2014
	Sort option: from right or from left - doesn't handle unicode properly yet
1.4	Sep 2012
	Adjusted batch file
1.2	May 2012
	Rearranged HTML
	Compatible with IE







--><!DOCTYPE xsl:stylesheet  [
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
<title>Glossy: <xsl:value-of select="Lexicon/Language/text()"/> Lexicon</title>

<script type="text/javascript" src="jquery-3.6.3.min.js"></script>
<script type="text/javascript" src="jquery.tablesorter/jquery.tablesorter.min.js"></script>
<script type="text/javascript" src="jquery.tablesorter/jquery.metadata.js"></script>
<link href="jquery.tablesorter/themes/blue/style.css" rel="stylesheet" type="text/css"></link>
<link href="glossy.css" rel="stylesheet" type="text/css"></link>
<link rel="icon"  type="image/png"  href="glossy64.png" />
<link rel="icon"  type="image/png"  href="glossy16.png" />

<!-- in case the output file is stored in a folder -->
<script type="text/javascript" src="../jquery-3.6.3.min.js"></script>
<script type="text/javascript" src="../jquery.tablesorter/jquery.tablesorter.min.js"></script>
<script type="text/javascript" src="../jquery.tablesorter/jquery.metadata.js"></script>
<link href="../jquery.tablesorter/themes/blue/style.css" rel="stylesheet" type="text/css"></link>
<link href="../glossy.css" rel="stylesheet" type="text/css"></link>
<link rel="icon"  type="image/png"  href="../glossy64.png" />
<link rel="icon"  type="image/png"  href="../glossy16.png" />
</head>
<body>
<div id="search"><span class="clearme" title="Clear" onclick="unsearch()">X</span><input id="search_target" type="text" title="Type text here to search for it. Press esc to show everything again. Double-click me to toggle sort from right or left." /><div id="search_tip">&nbsp;</div></div>
<div id="lexicon">
<table class="tablesorter" contextmenu="otheroptions"><thead><tr><th title="Target"><xsl:value-of select="Lexicon/Language/text()"/>
</th><th>Gloss</th></tr></thead>
<tbody>
<xsl:for-each select="//Sense">

<tr>
<xsl:attribute name="class"><xsl:value-of select="../../Lexeme/@Type"/> GL<xsl:value-of select="Gloss/@Language"/></xsl:attribute>
<td>
<xsl:attribute name="title"><xsl:value-of select="../../Lexeme/@Type"/></xsl:attribute>
<xsl:attribute name="class">v <xsl:value-of select="../../Lexeme/@Type"/></xsl:attribute>
	<xsl:value-of select="../../Lexeme/@Form"/>
	<xsl:if test="not(number(../../Lexeme/@Homograph)=1)">
		<span class="hm"><xsl:value-of select="../../Lexeme/@Homograph"/></span>
	</xsl:if>
</td><td>
<xsl:attribute name="class">g <xsl:value-of select="../../Lexeme/@Type"/> GL<xsl:value-of select="Gloss/@Language"/></xsl:attribute>
<xsl:attribute name="title"><xsl:value-of select="Gloss/@Language"/></xsl:attribute>
<xsl:value-of select="Gloss/text()"/></td></tr>

</xsl:for-each>
</tbody>
</table>
</div>
<script type="text/javascript">
var sort_order = "l";
var sorted_from_right_note = " [sorted from the end]";

$(function () {
	var delayed_search_set = false;
	var myTextExtraction = function(node) {
		return $(node).text();
	}
	$(".tablesorter").tablesorter({textExtraction: myTextExtraction, sortList: [[0,0],[1,0]]});
	//$(".tablesorter").tablesorter({sortList: [[0,0],[1,0]]});

	$("input").dblclick( toggle_sort_direction );
	$("input").focus( function () { $(this).addClass("active"); } )
		.blur( function () { $(this).removeClass("active"); } )
		.keyup( function (e) {
			search_text_verbatim = $(this).val();
			search_text = sort_search_equivs(search_text_verbatim);
			search_criteria = "";

			// special handling for special keys: escape (clear all) and backspace (delayed re-search)
			switch (e.keyCode) {
				case 27:
					unsearch(); return; break;
				case 8:
					if (!delayed_search_set) {
						delayed_search_set = true;
						window.setTimeout("delayed_search()", 2000);
					}
			}

			language_name = $("thead tr th:first").text();
			if (search_text.length==0) {
				// display all, when we clear the search box
				unsearch();
			} else if (search_text[0]=="*") {
				// search for glosses beginning with * (wrong spellings?)
				$(".tablesorter tbody tr").hide().each( function () {
					field_text = sort_search_equivs($(this).children("td:eq(1)").text());
					if (field_text.indexOf(search_text)>=0) {
						$(this).show();
					}
				});
			}  else if (search_text[0]=="?") {
				// search for glosses or enrties with a ?

			} else if (search_text.length==1) {
				// type a single char and find all the TARGET language words BEGINNING with that char
				$(".tablesorter tbody tr").hide().each( function () {
					field_text = sort_search_equivs($(this).children("td:first").text());
					if (field_text.indexOf(search_text)==0) {
						$(this).show();
					}
				});
				search_criteria = language_name+" words start "+search_text+"...";
				displayed = $(".tablesorter tbody tr:visible").length;

				// If the display is blank because nothing starts with this letter then try
				// displaying what glosses begin with this letter, at least.
				// May want to expand this or remove it.
				if (displayed==0) {
					$(".tablesorter tbody tr").hide().each( function () {
						field_text = sort_search_equivs($(this).children("td:eq(1)").text());
						if (sort_search_equivs.indexOf(search_text)==0) {
							$(this).show();
						}
					} );
					search_criteria = "glosses start "+search_text+"... (but no "+language_name+" words start with that)";
					displayed = $(".tablesorter tbody tr:visible").length;
				}
			} else {
				// normally, we search every row and every cell in each row for some text we want
				// then highlight the search text found with a span that gets deleted when we unsearch
				$(".tablesorter tbody tr").hide().each( function () {
					tr = $(this);
					$(this).children("td").each( function () {
						this_cell_verbatim = $(this).text();	// do all translation of equivalents first (eg a underline -> schwa)
						this_cell = this_cell_verbatim; //sort_search_equivs(this_cell_verbatim);	// do all translation of equivalents first (eg a underline -> schwa)
						left_pos = this_cell.search(search_text);	// see whether the equivalent search is found in the equivalent source.
						if (left_pos!=-1) {
							tr.show();
							//highlighted = this_cell_verbatim.replace(search_text, function (x) { return '<span class="highlight">'+x+'</span>'; } );
							/*
							Highlighting the results is a nightmare because we don't want to mess up the source of the search text for future searches.
							For now I've abandoned my efforts. The span class highlight is supposed to help with this.


							reWithCaptureGroup = new RegExp("("+search_text+")","");
							found_text = this_cell_verbatim.replace(reWithCaptureGroup, "$1" );

							new_span = document.createElement("span");
							new_span.className = "highlight";
							new_span.innerHTML = found_text;
							//new_span.innerHTML = this_cell.substr(left_pos,left_pos+found_text.length); //

							before_text = this_cell.substr(0,left_pos);
							after_text = this_cell.substr(left_pos+found_text.length);
							$(this).html(before_text);
							this.appendChild(new_span);
							$(this).append(after_text);
							*/
						}
					});
				});
				search_criteria = "words or glosses contain '"+search_text+"'"
			}
			total = $(".tablesorter tbody tr").length;
			displayed = $(".tablesorter tbody tr:visible").length;
			sort_note="";
			if (sort_order=="r") { sort_note = sorted_from_right_note; }
			window.status = (displayed+" of "+total+" "+search_criteria+sort_note);
			$("#search_tip").html(displayed+sort_note);
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

	unsearch();
	maximise_table();
	$("#search_target").focus();
	$(window).resize( maximise_table );
	window.setTimeout( "maximise_table", 500 );
});

function maximise_table() {
	body_height = $(window).height()-$("div#search").height();
	if (body_height != 0) {
		$("div#lexicon").height(body_height).width($(window).width());
		//alert($(window).width()+" width vs "+$("div#lexicon").width()+";" +$(window).height()+ " height");
	}
}

function unsearch() {
	$("#search_target").val("");
	$(".tablesorter tr").show();
	$(".highlight").removeClass("highlight");
	total = $(".tablesorter tbody tr").length;
	sort_note = "";
	if (sort_order=="r") { sort_note = sorted_from_right_note; }
	window.status = (total + " entries"+sort_note);
	$("#search_tip").html("Total words: "+total+sort_note);
	$("#search").click();
}

function delayed_search() {
	var delayed_search_set;
	delayed_search_set = false;
	if ($("input").val()=="") {
		unsearch();
	}
}

function set_sort_direction(direction) {
	myTextExtractionR = function(node) {
		// extract data from markup and return it
		return sort_search_equivs($(node).text().split("").reverse().join(""));
	}
	myTextExtraction = function(node) {
		return sort_search_equivs($(node).text());
	}

	sort_order = direction;
	if (direction=="r") {
		$("body").addClass("sort_right");
		//$("#search_target").addClass("sort_right");
		//$(".tablesorter").addClass("sort_right");
		$(".tablesorter").tablesorter({textExtraction: myTextExtractionR, sortList: [[0,0],[1,0]]});
		$("#search_tip").append(sorted_from_right_note);
	} else {
		$("body").removeClass("sort_right");
		//$("#search_target").removeClass("sort_right");
		//$(".tablesorter").removeClass("sort_right");
		$(".tablesorter").tablesorter({textExtraction: myTextExtraction, sortList: [[0,0],[1,0]]});
		if($("#search_tip").html().indexOf(sorted_from_right_note)!=-1) {
			$("#search_tip").html($("#search_tip").html().substring(0,$("#search_tip").html().indexOf(sorted_from_right_note)));
		}
	}

	if (parent.frames["nav"] != undefined) {
		parent.frames["nav"].document.getElementById("sort_menu").value = direction;
	}
}

/* Hardcoded for Gworog. Temporary feature 1.6 to be expanded and generalised later. */
function sort_search_equivs(inp) {


	/*equivalents =  [["a̱","i̱"], ["ə","ɨ"]];
	equiv_count = equivalents[0].length;
	output = inp.toLowerCase();
	i=0;
//	while( i != equiv_count ) {
		look_for = new RegExp(equivalents[0][i],"g");
		output = output.replace(look_for,equivalents[1][i]);
		i++;
//	}
		look_for = new RegExp(equivalents[0][i],"g");
		output = output.replace(look_for,equivalents[1][i]);

	if (inp[0]=="~") {

	} else if (inp[0]=="*") {

	}*/
	output = inp;
	return output;
}

function toggle_sort_direction() {
	if (sort_order=="l") {
		set_sort_direction("r");
	} else {
		set_sort_direction("l");
	}
}
</script>
</body>
</html>
</xsl:template>
</xsl:stylesheet>

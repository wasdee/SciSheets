<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd"><html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8">
        <title>Example: Context Menu (YUI Library)</title>

        <!-- Standard reset and fonts -->

        <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.9.0/build/reset/reset.css">
        <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.9.0/build/fonts/fonts.css">
 

        <!-- CSS for Menu -->

        <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.9.0/build/menu/assets/skins/sam/menu.css"> 


        <!-- Page-specific styles -->

        <style type="text/css">

            h1 { 

                font-weight: bold; 
                margin: 0 0 1em 0;
            }

            body {
            
                padding: 1em;
            
            }

            p, ul {

                margin: 1em 0;

            }

            p em,
            #operainstructions li em {

                font-weight: bold;

            }

            #operainstructions {

                list-style-type: square;
                margin-left: 2em;

            }

            #clones {

                background: #99cc66 url(assets/grass.png);

                /* Hide the alpha PNG from IE 6 */
                _background-image: none;

                width: 450px;
                height: 400px;
                overflow: auto;
         
            }
            
            #clones li {
            
                float: left;
                display: inline;
                border: solid 1px #000;
                background-color: #fff;
                margin: 10px;
                text-align: center;
                zoom: 1;
            
            }

            #clones li img {
            
                border: solid 1px #000;
                margin: 5px;
            
            }
            
            #clones li cite {
            
                display: block;
                text-align: center;
                margin: 0 0 5px 0;
                padding: 0 5px;

            }
            
        </style>

        <!-- Namespace source file -->

        <script type="text/javascript" src="http://yui.yahooapis.com/2.9.0/build/yahoo/yahoo.js"></script>


        <!-- Dependency source files -->

        <script type="text/javascript" src="http://yui.yahooapis.com/2.9.0/build/event/event.js"></script>
        <script type="text/javascript" src="http://yui.yahooapis.com/2.9.0/build/dom/dom.js"></script>
        <script type="text/javascript" src="http://yui.yahooapis.com/2.9.0/build/animation/animation.js"></script>
        

        <!-- Container source file -->

        <script type="text/javascript" src="http://yui.yahooapis.com/2.9.0/build/container/container_core.js"></script>


        <!-- Menu source file -->

        <script type="text/javascript" src="http://yui.yahooapis.com/2.9.0/build/menu/menu.js"></script>


        <!-- Page-specific script -->

        <script type="text/javascript">

            /*
                 Initialize the ContextMenu instances when the the elements 
                 that trigger their display are ready to be scripted.
            */

            YAHOO.util.Event.onContentReady("clones", function () {

                // Maintain a reference to the "clones" <ul>

                var oClones = this;


                // Clone the first ewe so that we can create more later

                var oLI = oClones.getElementsByTagName("li")[0];
                var oEweTemplate = oLI.cloneNode(true);


                // Renames an "ewe"
    
                function editEweName(p_oLI) {
    
                    var oCite = p_oLI.lastChild;
    

                    if (oCite.nodeType != 1) {
                    
                        oCite = oCite.previousSibling;
    
                    }
                
                    var oTextNode = oCite.firstChild;
    
                    var sName = window.prompt("Enter a new name for ", 
                                oTextNode.nodeValue);
    

                    if (sName && sName.length > 0) {
                        
                        oTextNode.nodeValue = sName;
    
                    }
                
                }
                
    
                // Clones an "ewe"
    
                function cloneEwe(p_oLI, p_oMenu) {

                    var oClone = p_oLI.cloneNode(true);
    
                    p_oLI.parentNode.appendChild(oClone);

                    p_oMenu.cfg.setProperty("trigger", oClones.childNodes);
                
                }
                
    
                // Deletes an "ewe"
    
                function deleteEwe(p_oLI) {
    
                    var oUL = p_oLI.parentNode;
    
                    oUL.removeChild(p_oLI);
                
                }
                
    
                // "click" event handler for each item in the ewe context menu
                
                function onEweContextMenuClick(p_sType, p_aArgs) {
    
                    /*
                         The second item in the arguments array (p_aArgs) 
                         passed back to the "click" event handler is the 
                         MenuItem instance that was the target of the 
                         "click" event.
                    */

                    var oItem = p_aArgs[1], // The MenuItem that was clicked
                    	oTarget = this.contextEventTarget,
                        oLI;


                    if (oItem) {

						oLI = oTarget.nodeName.toUpperCase() == "LI" ? 
								oTarget : YAHOO.util.Dom.getAncestorByTagName(oTarget, "LI");


                        switch (oItem.index) {
                        
                            case 0:     // Edit name
        
                                editEweName(oLI);
                            
                            break;
        
        
                            case 1:     // Clone
        
                                cloneEwe(oLI, this);
        
                            break;
                            
        
                            case 2:     // Delete
        
                                deleteEwe(oLI);
        
                            break;                    
                        
                        }
                    
                    }
                
                }


                /*
                     Array of text labels for the MenuItem instances to be
                     added to the ContextMenu instanc.
                */

                var aMenuItems = ["Edit Name", "Clone", "Delete" ]; 


                /*
					Instantiate a ContextMenu:  The first argument passed to the constructor
					is the id for the Menu element to be created, the second is an 
					object literal of configuration properties.
                */

                var oEweContextMenu = new YAHOO.widget.ContextMenu(
                                            "ewecontextmenu", 
                                            {
                                                trigger: oClones.childNodes,
                                                itemdata: aMenuItems,
                                                lazyload: true                                    
                                            } 
                                        );


                // "render" event handler for the ewe context menu

                function onContextMenuRender(p_sType, p_aArgs) {
    
                    //  Add a "click" event handler to the ewe context menu
    
                    this.subscribe("click", onEweContextMenuClick);
                
                }


                // Add a "render" event handler to the ewe context menu

                oEweContextMenu.subscribe("render", onContextMenuRender);


                // Deletes an ewe from the field

                function deleteEwes() {

                    oEweContextMenu.cfg.setProperty("target", null);

                    oClones.innerHTML = "";


                    function onHide(p_sType, p_aArgs, p_oItem) {

                        p_oItem.cfg.setProperty("disabled", true);
                    
                        p_oItem.parent.unsubscribe("hide", onHide, p_oItem);
                    
                    }

                    this.parent.subscribe("hide", onHide, this);

                }


                // Creates a new ewe and appends it to the field

                function createNewEwe() {
                
                    var oLI = oEweTemplate.cloneNode(true);
                    
                    oClones.appendChild(oLI);

                    this.parent.getItem(1).cfg.setProperty("disabled", false);

                    oEweContextMenu.cfg.setProperty("trigger", oClones.childNodes);
                
                }


                // Sets the color of the grass in the field

                function setFieldColor(p_sType, p_aArgs, p_sColor) {

                    var oCheckedItem = this.parent.checkedItem;

                    if (oCheckedItem != this) {

                        YAHOO.util.Dom.setStyle("clones", "backgroundColor", p_sColor);
                        
                        this.cfg.setProperty("checked", true);


                        oCheckedItem.cfg.setProperty("checked", false);

                        this.parent.checkedItem = this;
                    
                    }

                }


                // "render" event handler for the field context menu

                function onFieldMenuRender(p_sType, p_aArgs) {

                    if (this.parent) {  // submenu

                        this.checkedItem = this.getItem(0);

                    }

                }


                /*
                     Array of object literals - each containing configuration 
                     properties for the items for the context menu.
                */

                var oFieldContextMenuItemData = [
                
                    {
                        text: "Field color", 
                        submenu: { 
                            id: "fieldcolors", 
                            itemdata: [
                                { text: "Light Green", onclick: { fn: setFieldColor, obj: "#99cc66" }, checked: true }, 
                                { text: "Medium Green", onclick: { fn: setFieldColor, obj: "#669933" } }, 
                                { text: "Dark Green", onclick: { fn: setFieldColor, obj: "#336600" } }
                            ] 
                        } 
                    },
                    { text: "Delete all", onclick: { fn: deleteEwes } },
                    { text: "New Ewe", onclick: { fn: createNewEwe } }
                
                ];


                /*
					Instantiate a ContextMenu:  The first argument passed to the constructor
					is the id for the Menu element to be created, the second is an 
					object literal of configuration properties.
                */

                var oFieldContextMenu = new YAHOO.widget.ContextMenu(
                                                "fieldcontextmenu",
                                                {
                                                    trigger: "clones",
                                                    itemdata: oFieldContextMenuItemData,
                                                    lazyload: true
                                                }
                                            );


                // Add a "render" event handler to the field context menu

                oFieldContextMenu.subscribe("render", onFieldMenuRender);
            
            
            });
                    
        </script>

    </head>
    <body class="yui-skin-sam">

        <ul id="clones">
            <li><a href="http://en.wikipedia.org/wiki/Dolly_%28clone%29"><img src="assets/dolly.jpg" width="100" height="100" alt="Dolly, a ewe, the first mammal to have been successfully cloned from an adult cell."></a><cite>Dolly</cite></li>
        </ul>

    </body>
</html>

<!-- SpaceID=0 robot -->

<!-- VER-3.0.235613 -->
<!-- doc3.ydn.gq1.yahoo.com compressed/chunked Tue Jul 30 21:13:52 PDT 2013 -->


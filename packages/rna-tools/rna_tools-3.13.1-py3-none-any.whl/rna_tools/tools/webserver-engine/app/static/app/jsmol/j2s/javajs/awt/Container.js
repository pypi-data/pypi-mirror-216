Clazz.declarePackage ("javajs.awt");
Clazz.load (["javajs.awt.Component"], "javajs.awt.Container", ["JU.Lst"], function () {
c$ = Clazz.decorateAsClass (function () {
this.list = null;
this.cList = null;
Clazz.instantialize (this, arguments);
}, javajs.awt, "Container", javajs.awt.Component);
Clazz.defineMethod (c$, "getComponent", 
function (i) {
return this.list.get (i);
}, "~N");
Clazz.defineMethod (c$, "getComponentCount", 
function () {
return (this.list == null ? 0 : this.list.size ());
});
Clazz.defineMethod (c$, "getComponents", 
function () {
if (this.cList == null) {
if (this.list == null) return  new Array (0);
this.cList = this.list.toArray ();
}return this.cList;
});
Clazz.defineMethod (c$, "add", 
function (component) {
return this.addComponent (component);
}, "javajs.awt.Component");
Clazz.defineMethod (c$, "addComponent", 
function (component) {
if (this.list == null) this.list =  new JU.Lst ();
this.list.addLast (component);
this.cList = null;
component.parent = this;
return component;
}, "javajs.awt.Component");
Clazz.defineMethod (c$, "insertComponent", 
function (component, index) {
if (this.list == null) return this.addComponent (component);
this.list.add (index, component);
this.cList = null;
component.parent = this;
return component;
}, "javajs.awt.Component,~N");
Clazz.defineMethod (c$, "remove", 
function (i) {
var c = this.list.remove (i);
c.parent = null;
this.cList = null;
}, "~N");
Clazz.defineMethod (c$, "removeAll", 
function () {
if (this.list != null) {
for (var i = this.list.size (); --i >= 0; ) this.list.get (i).parent = null;

this.list.clear ();
}this.cList = null;
});
Clazz.defineMethod (c$, "getSubcomponentWidth", 
function () {
return (this.list != null && this.list.size () == 1 ? this.list.get (0).getSubcomponentWidth () : 0);
});
Clazz.defineMethod (c$, "getSubcomponentHeight", 
function () {
return (this.list != null && this.list.size () == 1 ? this.list.get (0).getSubcomponentHeight () : 0);
});
});

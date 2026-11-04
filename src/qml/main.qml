import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 360
    height: 640
    title: qsTr("VYAS Astrology")

    // Placeholder UI – replace with real charts later
    Column {
        anchors.centerIn: parent
        spacing: 20
        Text { text: qsTr("Welcome to VYAS") }
        Button { text: qsTr("Run demo"); onClicked: console.log("demo") }
    }
}

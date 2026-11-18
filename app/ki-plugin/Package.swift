// swift-tools-version: 5.9
import PackageDescription

// Lokale KI für den Trainingslog (Capacitor-Plugin). Name muss zu „trainingslog-ki“ passen (Capacitor macht daraus TrainingslogKi).
let package = Package(
    name: "TrainingslogKi",
    platforms: [.iOS(.v15)],
    products: [
        .library(name: "TrainingslogKi", targets: ["TrainingslogKiPlugin"])
    ],
    dependencies: [
        .package(url: "https://github.com/ionic-team/capacitor-swift-pm.git", from: "8.0.0")
    ],
    targets: [
        .target(
            name: "TrainingslogKiPlugin",
            dependencies: [
                .product(name: "Capacitor", package: "capacitor-swift-pm"),
                .product(name: "Cordova", package: "capacitor-swift-pm")
            ],
            path: "ios/Sources/TrainingslogKiPlugin"
        )
    ]
)

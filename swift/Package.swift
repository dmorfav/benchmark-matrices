// swift-tools-version:5.3
import PackageDescription

let package = Package(
    name: "BenchmarkMatrices",
    platforms: [
        .macOS(.v10_15)
    ],
    products: [
        .executable(name: "benchmark", targets: ["Benchmark"])
    ],
    targets: [
        .target(
            name: "Benchmark",
            path: "Sources/Benchmark",
            sources: ["main.swift"]
        )
    ]
)

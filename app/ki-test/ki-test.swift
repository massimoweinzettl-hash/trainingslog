// KI-Testlauf für „Frag die App“ (seit v204): stellt Apples On-Device-Modell auf dem Mac alle Fragen aus fragen.json
// – mit denselben Anweisungen und Daten wie die App – und schreibt die Antworten nach antworten.txt / antworten.json.
// Voraussetzung: macOS 26, Apple Intelligence an, Xcode 26.  Aufruf (im Ordner trainingslog):  swift app/ki-test/ki-test.swift
// fragen.json erzeugt Claude mit app/ki-test/fragen-bauen.py (Beispieldaten aus app/tests/rundgang.py).
import Foundation
import FoundationModels

struct Frage: Codable { let id: String; let q: String; let soll: String; let instructions: String; let prompt: String; let fest: String? }
struct Antwort: Codable { let id: String; let q: String; let soll: String; let a: String; let sek: Double }

let dir = URL(fileURLWithPath: CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "app/ki-test")
let fragen = try JSONDecoder().decode([Frage].self, from: Data(contentsOf: dir.appendingPathComponent("fragen.json")))

switch SystemLanguageModel.default.availability {
case .available: print("Modell bereit, \(fragen.count) Fragen …")
case .unavailable(let why): print("Modell nicht verfügbar: \(why)"); exit(1)
}

var out: [Antwort] = []
for f in fragen {
    let t0 = Date()
    var a: String
    if let fest = f.fest, !fest.isEmpty {
        a = "(feste Antwort der App, ohne Modell) " + fest
    } else { do {
        let s = LanguageModelSession(instructions: f.instructions)
        a = try await s.respond(to: f.prompt, options: GenerationOptions(temperature: 0.2, maximumResponseTokens: 350)).content
    } catch {
        a = "FEHLER: \(error)"
    } }
    let sek = (Date().timeIntervalSince(t0) * 10).rounded() / 10
    out.append(Antwort(id: f.id, q: f.q, soll: f.soll, a: a, sek: sek))
    print("✓ \(f.id) (\(sek) s) \(f.q)")
}

let enc = JSONEncoder(); enc.outputFormatting = [.prettyPrinted, .withoutEscapingSlashes]
try enc.encode(out).write(to: dir.appendingPathComponent("antworten.json"))
let txt = out.map { "[\($0.id)] \($0.q)\nSOLL: \($0.soll)\nIST:  \($0.a)\n" }.joined(separator: "\n")
try txt.write(to: dir.appendingPathComponent("antworten.txt"), atomically: true, encoding: .utf8)
print("Fertig: app/ki-test/antworten.txt")

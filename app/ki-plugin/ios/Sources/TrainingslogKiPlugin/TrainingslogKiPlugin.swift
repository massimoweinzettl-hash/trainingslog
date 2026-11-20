import Foundation
import UIKit
import WebKit
import Capacitor
#if canImport(FoundationModels)
import FoundationModels
#endif

/// „Frag die App“: Apples On-Device-Sprachmodell (Foundation Models, iOS 26) für den Trainingslog.
/// JS-Name „Ki“, Aufruf aus index.html über Capacitor.nativePromise("Ki", "status" | "ask").
/// Antworten: { ok: true, text } oder { ok: false, reason: ios|device|off|loading|long|guard|lang|other, msg? }.
/// v196: neu geschrieben, die Datei aus v182 war wegen `ios/` in .gitignore nie im Repo.
@objc(TrainingslogKiPlugin)
public class TrainingslogKiPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "TrainingslogKiPlugin"
    public let jsName = "Ki"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "status", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "ask", returnType: CAPPluginReturnPromise)
    ]

    /// v230 (Wunsch des Nutzers): iOS 26 legt oben (und unten) einen weichen Unschärfe-Verlauf über die Web-Ansicht
    /// („Scroll Edge Effect“), dadurch werden Zahnrad, KI und Glocke unscharf. Hier abgeschaltet, sobald das Plugin lädt.
    override public func load() {
        #if canImport(FoundationModels)
        if #available(iOS 26.0, *) {
            DispatchQueue.main.async { [weak self] in
                guard let sv = self?.bridge?.webView?.scrollView else { return }
                sv.topEdgeEffect.isHidden = true
                sv.bottomEdgeEffect.isHidden = true
            }
        }
        #endif
    }

    /// nil = Modell bereit, sonst Grund für die App.
    private func notReadyReason() -> String? {
        #if canImport(FoundationModels)
        if #available(iOS 26.0, *) {
            switch SystemLanguageModel.default.availability {
            case .available:
                return nil
            case .unavailable(let why):
                switch why {
                case .deviceNotEligible: return "device"
                case .appleIntelligenceNotEnabled: return "off"
                case .modelNotReady: return "loading"
                @unknown default: return "other"
                }
            @unknown default:
                return "other"
            }
        }
        #endif
        return "ios"
    }

    @objc func status(_ call: CAPPluginCall) {
        if let why = notReadyReason() {
            call.resolve(["ok": false, "reason": why])
        } else {
            call.resolve(["ok": true])
        }
    }

    @objc func ask(_ call: CAPPluginCall) {
        let instructions = call.getString("instructions") ?? ""
        let prompt = call.getString("prompt") ?? ""
        if prompt.isEmpty {
            call.resolve(["ok": false, "reason": "other", "msg": "Keine Frage übergeben."])
            return
        }
        if let why = notReadyReason() {
            call.resolve(["ok": false, "reason": why])
            return
        }
        #if canImport(FoundationModels)
        if #available(iOS 26.0, *) {
            Task {
                do {
                    // Neue Sitzung je Frage: kein Verlauf, damit der kleine Kontext (4096 Token) reicht.
                    let session = LanguageModelSession(instructions: instructions)
                    let options = GenerationOptions(temperature: 0.2, maximumResponseTokens: 350)
                    let answer = try await session.respond(to: prompt, options: options)
                    call.resolve(["ok": true, "text": answer.content])
                } catch let err as LanguageModelSession.GenerationError {
                    var reason = "other"
                    switch err {
                    case .exceededContextWindowSize: reason = "long"
                    case .guardrailViolation: reason = "guard"
                    case .unsupportedLanguageOrLocale: reason = "lang"
                    case .assetsUnavailable: reason = "loading"
                    default: reason = "other"
                    }
                    call.resolve(["ok": false, "reason": reason, "msg": err.localizedDescription])
                } catch {
                    call.resolve(["ok": false, "reason": "other", "msg": error.localizedDescription])
                }
            }
            return
        }
        #endif
        call.resolve(["ok": false, "reason": "ios"])
    }
}

# Motion repositories — audited routing catalog

Source: [@Mnilax's 15-repo X post](https://x.com/mnilax/status/2109314840057565345). Repositories were inspected read-only at the linked commits. This is **not** an endorsement of the post's author-identity, performance, speed or cost claims. Static license/tree review is not a full security audit. Follow the latest upstream terms before commercial deployment.

**Packaging key:** *Bundled* = this repo redistributes selected Markdown under the upstream MIT license; *reference* = link only, no code or scripts installed. The default installer installs only this original routing skill. `--official` adds selected official LottieFiles and GSAP skills; see README for exactly what that means.

## Launch video and footage editing

1. [product-launch-motion](https://github.com/AbubakrChan/product-launch-motion/tree/951d6149d2748a15058f79dcf8e8c4bf00824121) — **reference** (MIT skill; FFmpeg/GSAP/render helpers and third-party imagery need separate review and rights).
2. [motion-graphics-skills](https://github.com/charlie947/motion-graphics-skills/tree/229022ebca76972e119e36ada23a1648d51665ab) — **reference** (MIT; 15 skills, some project writes; bundled ZIPs not audited).
3. [claude-motion-design](https://github.com/howseen-ai/claude-motion-design/tree/3d90d349ef3fdde9b7e89de4df4a2159c9e8697f) — **reference** (MIT; personal paths, media download helper and a key-bearing API helper; not portable as-is).
4. [hyperframes-student-kit](https://github.com/nateherkai/hyperframes-student-kit/tree/0d30152a82b9ceb93cfdd9bdbf46f0d5ab3cde86) — **reference** (MIT software; brand assets excluded; some scripts can upload footage or use paid generation).
5. [motion-graphics](https://github.com/Barty-Bart/motion-graphics/tree/83355bb58f78cdb486d6a00f6cfa22e40e538f03) — **reference** (MIT software; setup scripts install browser/Python dependencies and object separation downloads large models).

## Animated shorts and web animation

6. [animate](https://github.com/cth9191/animate/tree/7e5eb56feb2dd573f890e1b7b34748af43d58263) — **reference** (MIT; useful storyboarding skill but linked templates/tools, browser/FFmpeg and optional voice services make a partial copy misleading).
7. [claude-motion](https://github.com/whaleyxbt/claude-motion/tree/e627941543d9988b155dc610bb9cc0115a5e365e) — **reference** (MIT; project-specific toolkit, not drop-in global skills).
8. [claude-remotion-skill](https://github.com/haidrrrry/claude-remotion-skill/tree/1dcbe5e3fc6cf970bd10d3cc05f0a8a5d19d0383) — **reference** (MIT; React/Remotion/Chromium project required; review linked guides and license).
9. [Motion](https://github.com/motiondivision/motion/tree/e6bf03ead39cae7a2c5f8fe902ce8a9c1a9a22e8) — **reference** (MIT animation library; internal skills concern its own monorepo and can propose PR publication).
10. [motion-dev-animations-skill](https://github.com/199-biotechnologies/motion-dev-animations-skill/tree/3feedfb4dba8adae40fc9a5f9a23e3dda2121205) — **reference** (MIT skill; requires supporting examples/templates and a project using Motion; don't run its validator automatically).

## Official framework and motion guidance

11. [HeyGen HyperFrames](https://github.com/heygen-com/hyperframes/tree/d0b551d0330d4d2cd932348a911b5457ed1ed3c8) — **reference** (Apache-2.0; rendering and asset sourcing require platform-specific runtime and human approval).
12. [Remotion monorepo](https://github.com/remotion-dev/remotion/tree/de2fd2428c94b282d692181a275d213ecc03a062) — **reference only** (the monorepo uses custom, use-restricted license terms; not a general redistribution grant).
13. [Remotion skills](https://github.com/remotion-dev/skills/tree/32b241b97f4e0e4ab61fe9a41b05e6e64503f8c5) — **reference only** (no repository LICENSE found at audit; 12 skills have nested references; don't repackage without permission).
14. [GSAP skills](https://github.com/greensock/gsap-skills/tree/aed9cfd3277740755f6bfc1155c7aa645403b760) — **bundled opt-in** (eight MIT Markdown skills; GSAP runtime/plugins have their own terms and must be selected per project).
15. [LottieFiles motion-design-skill](https://github.com/LottieFiles/motion-design-skill/tree/f9a8a041b85185ee4881b3471d3415e939aac772) — **bundled opt-in** (one MIT skill with all 16 supporting text/reference files; its `name` was changed to `lottiefiles-motion-design` here to avoid collisions with existing `motion-design` skills).

**Choose one route:** storyboard/launch → 1–3; footage/shorts → 4–8; web UI → 9–10 or 14; Remotion project → 8 or 12–13 (consult upstream directly); broad motion taste/principles → 15. Licenses, package dependencies and service pricing may change after the pinned audit.

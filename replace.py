import sys

with open('/Users/syedmustafaahmed/syed-portfolio/syed-portfolio/index.html', 'r') as f:
    text = f.read()

import re
pattern = re.compile(r'    const ArcCarousel = \(\{ videos \}\) => \{.*?(?=    const rootNode = document\.getElementById)', re.DOTALL)

new_content = """    const ArcCarousel = ({ videos }) => {
      const [activeIndex, setActiveIndex] = useState(4);
      const [isMobile, setIsMobile] = useState(false);
      const [playingId, setPlayingId] = useState(null);
      const [isDragging, setIsDragging] = useState(false);
      const [isHovering, setIsHovering] = useState(false);
      const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
      const lastWheelTime = useRef(0);

      useEffect(() => {
        const checkMobile = () => setIsMobile(window.innerWidth <= 768);
        checkMobile();
        window.addEventListener("resize", checkMobile);
        return () => window.removeEventListener("resize", checkMobile);
      }, []);

      useEffect(() => {
        if (!isMobile && videos[activeIndex] && !isDragging) {
          setPlayingId(videos[activeIndex].id);
        } else if (isDragging) {
          setPlayingId(null);
        }
      }, [activeIndex, isMobile, isDragging]);

      const handleWheel = (e) => {
        const now = Date.now();
        if (now - lastWheelTime.current < 400) return;
        if (Math.abs(e.deltaX) > 15 || Math.abs(e.deltaY) > 15) {
          lastWheelTime.current = now;
          if (e.deltaX > 0 || e.deltaY > 0) {
            if (activeIndex < videos.length - 1) setActiveIndex(activeIndex + 1);
          } else {
            if (activeIndex > 0) setActiveIndex(activeIndex - 1);
          }
        }
      };

      const handleMouseMove = (e) => {
        if (isMobile) return;
        const x = (e.clientX / window.innerWidth) - 0.5;
        const y = (e.clientY / window.innerHeight) - 0.5;
        setMousePos({ x, y });
      };

      const getTransform = (offset, mobile) => {
        if (mobile) {
          return `rotateY(${offset * 8}deg) translateZ(${80}px) scale(${offset === 0 ? 1 : 0.85})`;
        } else {
          return `rotateY(${offset * 16}deg) translateZ(${380}px) scale(${offset === 0 ? 1 : 0.82})`;
        }
      };

      const activeVideo = videos[activeIndex];

      return (
        <div 
          onMouseMove={handleMouseMove}
          onMouseEnter={() => setIsHovering(true)}
          onMouseLeave={() => setIsHovering(false)}
          style={{ 
            width: "100%", 
            display: "grid", 
            gridTemplateColumns: "repeat(12, minmax(0, 1fr))",
            alignItems: "center", 
            cursor: isDragging ? "grabbing" : (isHovering ? "grab" : "default")
          }}
        >
          {/* LEFT TEXT PANEL */}
          {!isMobile && (
            <div style={{ gridColumn: "span 3 / span 3", paddingLeft: "48px", paddingRight: "24px", zIndex: 20 }}>
              <AnimatePresence mode="wait">
                <motion.div
                  key={activeIndex}
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: mousePos.y * 6, x: mousePos.x * -6 }}
                  exit={{ opacity: 0, y: -15 }}
                  transition={{ opacity: { duration: 0.4 }, default: { type: "spring", stiffness: 70, damping: 22, mass: 1.1 } }}
                >
                  <div style={{ fontSize: "12px", textTransform: "uppercase", letterSpacing: "0.35em", color: "#6b7280", marginBottom: "12px" }}>
                    {activeVideo?.type}
                  </div>
                  <div style={{ fontSize: "18px", color: "#d1d5db", lineHeight: "1.6", maxWidth: "320px", textShadow: "0 0 20px rgba(255,255,255,0.1)" }}>
                    {activeVideo?.desc}
                  </div>
                </motion.div>
              </AnimatePresence>
            </div>
          )}

          {/* CENTER CAROUSEL (DRAG ANYWHERE) */}
          <motion.div 
            onWheel={handleWheel}
            drag="x"
            dragElastic={0.12}
            dragMomentum={true}
            onDragStart={() => setIsDragging(true)}
            onDragEnd={(event, info) => {
               setIsDragging(false);
               if (info.offset.x < -50) setActiveIndex((prev) => Math.min(prev + 1, videos.length - 1));
               if (info.offset.x > 50)  setActiveIndex((prev) => Math.max(prev - 1, 0));
            }}
            style={{ 
              gridColumn: isMobile ? "span 12 / span 12" : "span 6 / span 6",
              height: isMobile ? "450px" : "600px", 
              display: "flex", 
              justifyContent: "center", 
              alignItems: "center", 
              perspective: "1200px", 
              transformStyle: "preserve-3d",
              overflow: "hidden",
              position: "relative"
            }}
          >
            {/* Structural container to counter the forward translateZ */}
            <div style={{ width: "100%", height: "100%", position: "absolute", display: "flex", justifyContent: "center", alignItems: "center", transformStyle: "preserve-3d", transform: isMobile ? "translateZ(-80px)" : "translateZ(-380px)", pointerEvents: "none" }}>
              {videos.map((vid, index) => {
                const offset = index - activeIndex;
                const isActive = offset === 0;
                const isPlaying = playingId === vid.id;
                const videoRef = useRef(null);
                
                useEffect(() => {
                   if (videoRef.current) {
                      if (isPlaying) videoRef.current.play().catch(() => {});
                      else videoRef.current.pause();
                   }
                }, [isPlaying]);

                return (
                  <motion.div
                    key={vid.id + "_" + index}
                    layout
                    initial={false}
                    animate={{
                      transform: getTransform(offset, isMobile),
                      opacity: isActive ? 1 : Math.max(1 - (Math.abs(offset) * 0.2), 0.3),
                      filter: Math.abs(offset) > 1 ? "blur(3px)" : "blur(0px)",
                      zIndex: 10 - Math.abs(offset)
                    }}
                    transition={{ type: "spring", stiffness: 70, damping: 22, mass: 1.1 }}
                    onTap={() => {
                       if (!isActive) {
                          setActiveIndex(index);
                       } else if (isMobile) {
                          setPlayingId(prev => prev === vid.id ? null : vid.id);
                       }
                    }}
                    style={{
                      position: "absolute",
                      width: isMobile ? "180px" : "240px",
                      height: isMobile ? "320px" : "426px",
                      borderRadius: "16px",
                      overflow: "hidden",
                      boxShadow: isActive ? "0 0 40px rgba(100,150,255,0.35)" : "0 0 20px rgba(100,150,255,0.15)",
                      pointerEvents: "auto",
                      transformOrigin: "center center",
                      backgroundColor: "#000"
                    }}
                    whileTap={{ scale: isActive ? 0.98 : 0.82 }}
                  >
                    <video 
                      ref={videoRef}
                      src={vid.src} 
                      muted 
                      loop 
                      playsInline 
                      style={{ width: "100%", height: "100%", objectFit: "cover", display: "block" }} 
                    />
                    {!isActive && (
                      <div style={{ position: "absolute", inset: 0, background: "linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.2) 100%)", pointerEvents: "none" }} />
                    )}
                    {isActive && isMobile && (
                      <motion.div 
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        style={{ position: "absolute", bottom: "16px", left: "16px", right: "16px", background: "rgba(0,0,0,0.6)", backdropFilter: "blur(4px)", padding: "8px 12px", borderRadius: "8px", pointerEvents: "none" }}
                      >
                        <span style={{ color: "#fff", fontSize: "14px", fontWeight: "600", letterSpacing: "-0.2px" }}>{vid.title}</span>
                      </motion.div>
                    )}
                  </motion.div>
                );
              })}
            </div>
          </motion.div>

          {/* RIGHT TEXT PANEL */}
          {!isMobile && (
            <div style={{ gridColumn: "span 3 / span 3", paddingLeft: "24px", paddingRight: "48px", textAlign: "right", zIndex: 20 }}>
              <AnimatePresence mode="wait">
                <motion.div
                  key={activeIndex}
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: mousePos.y * 6, x: mousePos.x * 6 }}
                  exit={{ opacity: 0, y: -15 }}
                  transition={{ opacity: { duration: 0.4 }, default: { type: "spring", stiffness: 70, damping: 22, mass: 1.1 } }}
                >
                  <h3 style={{ fontSize: "48px", fontWeight: "600", letterSpacing: "-0.5px", marginBottom: "16px", lineHeight: "1.1", background: "linear-gradient(to right, #ffffff, #e5e7eb, #9ca3af)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
                    {activeVideo?.title}
                  </h3>
                  <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "flex-end", gap: "8px" }}>
                    {activeVideo?.tags.map(tag => (
                      <span key={tag} style={{ padding: "4px 16px", background: "transparent", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "999px", fontSize: "14px", color: "#d1d5db" }}>
                        {tag}
                      </span>
                    ))}
                  </div>
                </motion.div>
              </AnimatePresence>
            </div>
          )}
        </div>
      );
    };

"""

text = pattern.sub(new_content, text)

with open('/Users/syedmustafaahmed/syed-portfolio/syed-portfolio/index.html', 'w') as f:
    f.write(text)

print("Replacement successful")

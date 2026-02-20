/**
 * interactive.js -- Graph Theory Interactive Moments
 * Lecture 08: Graph Theory
 *
 * Three self-contained interactions for Reveal.js 5.1.0 slides:
 *   1. Six Degrees Path Tracer
 *   2. PageRank Ranking
 *   3. Network Architecture Builder
 *
 * Listens for Reveal.js `slidechanged` events to initialise/reset each
 * interaction when its slide becomes active.
 *
 * Colour palette (3Blue1Brown-inspired):
 *   bg-dark  #1b2631   bg-card  #1e3044   text     #ecf0f1
 *   blue     #3498db   yellow   #f1c40f   green    #2ecc71
 *   teal     #1abc9c   orange   #e67e22   red      #e74c3c
 */
(function () {
  'use strict';

  // ---------------------------------------------------------------
  // Shared palette
  // ---------------------------------------------------------------
  const C = {
    bgDark:  '#1b2631',
    bgCard:  '#1e3044',
    text:    '#ecf0f1',
    blue:    '#3498db',
    yellow:  '#f1c40f',
    green:   '#2ecc71',
    teal:    '#1abc9c',
    orange:  '#e67e22',
    red:     '#e74c3c',
    muted:   '#95a5a6',
  };

  // ---------------------------------------------------------------
  // SVG helper
  // ---------------------------------------------------------------
  const SVG_NS = 'http://www.w3.org/2000/svg';

  function svgEl(tag, attrs) {
    const el = document.createElementNS(SVG_NS, tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        el.setAttribute(k, attrs[k]);
      });
    }
    return el;
  }

  function htmlEl(tag, attrs) {
    const el = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === 'textContent') { el.textContent = attrs[k]; }
        else if (k === 'innerHTML') { el.innerHTML = attrs[k]; }
        else { el.setAttribute(k, attrs[k]); }
      });
    }
    return el;
  }

  // Inject a <style> block once for animations/utility classes shared
  // across all three interactions.
  function injectStyles() {
    if (document.getElementById('graph-interactive-styles')) return;
    var style = document.createElement('style');
    style.id = 'graph-interactive-styles';
    style.textContent = [
      '@keyframes pulse-node{0%,100%{r:35}50%{r:42}}',
      '@keyframes pulse-pr{0%,100%{opacity:1}50%{opacity:.6}}',
      '@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}',
      '.gi-shake{animation:shake .3s ease}',
      '.gi-pulse{animation:pulse-node 1.2s ease-in-out infinite}',
      '.gi-btn{',
      '  display:inline-block;padding:8px 18px;margin:4px;border:none;border-radius:6px;',
      '  font-size:14px;font-weight:600;cursor:pointer;color:#fff;',
      '  font-family:inherit;transition:opacity .2s}',
      '.gi-btn:hover{opacity:.85}',
      '.gi-btn-blue{background:' + C.blue + '}',
      '.gi-btn-yellow{background:' + C.yellow + ';color:#222}',
      '.gi-btn-green{background:' + C.green + '}',
      '.gi-btn-red{background:' + C.red + '}',
      '.gi-btn-orange{background:' + C.orange + '}',
      '.gi-btn-teal{background:' + C.teal + '}',
      /* PageRank drag chips & slots */
      '.pr-chip{',
      '  display:inline-flex;align-items:center;justify-content:center;',
      '  width:52px;height:36px;margin:4px;border-radius:8px;cursor:grab;',
      '  font-weight:700;font-size:16px;color:#fff;background:' + C.blue + ';',
      '  user-select:none;transition:transform .15s,box-shadow .15s}',
      '.pr-chip:active{cursor:grabbing;transform:scale(1.1);box-shadow:0 4px 12px rgba(0,0,0,.4)}',
      '.pr-chip.placed{opacity:.35;pointer-events:none}',
      '.pr-slot{',
      '  display:flex;align-items:center;justify-content:space-between;',
      '  width:100%;height:44px;margin:6px 0;padding:0 12px;box-sizing:border-box;',
      '  border:2px dashed ' + C.muted + ';border-radius:8px;',
      '  color:' + C.text + ';font-size:14px;font-weight:600;',
      '  transition:border-color .3s,background .3s}',
      '.pr-slot.filled{border-style:solid;background:rgba(255,255,255,.06)}',
      '.pr-slot .slot-label{pointer-events:none}',
      '.pr-slot .slot-value{pointer-events:none;font-size:13px;opacity:.7}',
      /* Architect results */
      '.arch-results{',
      '  margin-top:8px;padding:10px 14px;border-radius:8px;',
      '  background:rgba(255,255,255,.06);color:' + C.text + ';font-size:13px;line-height:1.6}',
      '.arch-results strong{color:' + C.yellow + '}',
    ].join('\n');
    document.head.appendChild(style);
  }

  // ===============================================================
  // 1. SIX DEGREES PATH TRACER
  // ===============================================================
  var sixDegreesInitialised = false;

  function initSixDegrees() {
    var container = document.getElementById('interactive-six-degrees');
    if (!container || sixDegreesInitialised) return;
    sixDegreesInitialised = true;
    container.innerHTML = '';

    // --- Data ---
    var nodes = [
      {id:'you',        label:'You',        x:100, y:300},
      {id:'friend',     label:'Friend',     x:250, y:150},
      {id:'classmate',  label:'Classmate',  x:250, y:450},
      {id:'teacher',    label:'Teacher',    x:400, y:100},
      {id:'coach',      label:'Coach',      x:400, y:300},
      {id:'parent',     label:'Parent',     x:400, y:500},
      {id:'journalist', label:'Journalist', x:600, y:200},
      {id:'athlete',    label:'Athlete',    x:600, y:400},
      {id:'agent',      label:'Agent',      x:750, y:300},
      {id:'celebrity',  label:'Celebrity',  x:900, y:300},
    ];
    var edges = [
      ['you','friend'],['you','classmate'],['friend','teacher'],['friend','coach'],
      ['classmate','coach'],['classmate','parent'],['teacher','journalist'],
      ['coach','athlete'],['coach','journalist'],['parent','athlete'],
      ['journalist','agent'],['athlete','agent'],['agent','celebrity'],
      ['teacher','coach'],['journalist','celebrity'],
    ];

    var nodeMap = {};
    nodes.forEach(function (n) { nodeMap[n.id] = n; });

    function adj(id) {
      var out = [];
      edges.forEach(function (e) {
        if (e[0] === id) out.push(e[1]);
        if (e[1] === id) out.push(e[0]);
      });
      return out;
    }

    // BFS shortest path
    function bfs(startId, endId) {
      var queue = [[startId]];
      var visited = {};
      visited[startId] = true;
      while (queue.length) {
        var path = queue.shift();
        var last = path[path.length - 1];
        if (last === endId) return path;
        adj(last).forEach(function (nb) {
          if (!visited[nb]) {
            visited[nb] = true;
            queue.push(path.concat(nb));
          }
        });
      }
      return null;
    }

    // --- State ---
    var currentPath = ['you'];
    var showingShortest = false;

    // --- SVG ---
    var svg = svgEl('svg', {
      viewBox: '0 0 1000 600',
      width: '100%',
      height: '100%',
      style: 'display:block;max-height:420px;',
    });
    container.appendChild(svg);

    // Edges group (below nodes)
    var edgeGroup = svgEl('g');
    svg.appendChild(edgeGroup);

    // Nodes group
    var nodeGroup = svgEl('g');
    svg.appendChild(nodeGroup);

    // Edge elements keyed by "id1--id2" (sorted)
    var edgeEls = {};
    edges.forEach(function (e) {
      var key = [e[0], e[1]].sort().join('--');
      var a = nodeMap[e[0]], b = nodeMap[e[1]];
      var line = svgEl('line', {
        x1: a.x, y1: a.y, x2: b.x, y2: b.y,
        stroke: C.muted, 'stroke-width': 2, 'stroke-opacity': 0.4,
      });
      edgeGroup.appendChild(line);
      edgeEls[key] = line;
    });

    // Node elements
    var nodeCircles = {};
    var nodeLabels = {};
    nodes.forEach(function (n) {
      var g = svgEl('g', {style: 'cursor:pointer'});

      var circle = svgEl('circle', {
        cx: n.x, cy: n.y, r: 35,
        fill: n.id === 'you' ? C.yellow : (n.id === 'celebrity' ? C.orange : C.blue),
        stroke: 'rgba(255,255,255,.15)', 'stroke-width': 2,
      });
      if (n.id === 'celebrity') {
        circle.classList.add('gi-pulse');
      }
      g.appendChild(circle);

      var txt = svgEl('text', {
        x: n.x, y: n.y + 5,
        fill: n.id === 'you' ? '#222' : '#fff',
        'text-anchor': 'middle',
        'font-size': n.label.length > 7 ? '11' : '13',
        'font-weight': '700',
        'pointer-events': 'none',
      });
      txt.textContent = n.label;
      g.appendChild(txt);

      nodeGroup.appendChild(g);
      nodeCircles[n.id] = circle;
      nodeLabels[n.id] = txt;

      g.addEventListener('click', function () { handleNodeClick(n.id); });
    });

    // Steps counter (top-right inside SVG)
    var stepsText = svgEl('text', {
      x: 970, y: 30,
      fill: C.text,
      'text-anchor': 'end',
      'font-size': '18',
      'font-weight': '700',
    });
    stepsText.textContent = 'Steps: 0';
    svg.appendChild(stepsText);

    // Buttons
    var btnRow = htmlEl('div', {style: 'text-align:center;margin-top:6px;'});
    var btnShortest = htmlEl('button', {class: 'gi-btn gi-btn-yellow', textContent: 'Show Shortest'});
    var btnReset = htmlEl('button', {class: 'gi-btn gi-btn-red', textContent: 'Reset'});
    btnRow.appendChild(btnShortest);
    btnRow.appendChild(btnReset);
    container.appendChild(btnRow);

    // --- Logic ---
    function updateVisuals() {
      stepsText.textContent = 'Steps: ' + (currentPath.length - 1);

      // Reset all nodes/edges to default look
      nodes.forEach(function (n) {
        var c = nodeCircles[n.id];
        if (n.id === 'you') {
          c.setAttribute('fill', C.yellow);
          nodeLabels[n.id].setAttribute('fill', '#222');
        } else if (n.id === 'celebrity') {
          c.setAttribute('fill', C.orange);
          nodeLabels[n.id].setAttribute('fill', '#fff');
        } else {
          c.setAttribute('fill', C.blue);
          nodeLabels[n.id].setAttribute('fill', '#fff');
        }
        c.classList.remove('gi-pulse');
      });

      Object.keys(edgeEls).forEach(function (k) {
        edgeEls[k].setAttribute('stroke', C.muted);
        edgeEls[k].setAttribute('stroke-width', 2);
        edgeEls[k].setAttribute('stroke-opacity', 0.4);
      });

      // Highlight path
      for (var i = 0; i < currentPath.length; i++) {
        var nid = currentPath[i];
        nodeCircles[nid].setAttribute('fill', C.green);
        nodeLabels[nid].setAttribute('fill', '#fff');
        if (i > 0) {
          var key = [currentPath[i - 1], currentPath[i]].sort().join('--');
          if (edgeEls[key]) {
            edgeEls[key].setAttribute('stroke', C.green);
            edgeEls[key].setAttribute('stroke-width', 4);
            edgeEls[key].setAttribute('stroke-opacity', 1);
          }
        }
      }

      // Keep "You" yellow-ish if it is first
      nodeCircles['you'].setAttribute('fill', currentPath.length === 1 ? C.yellow : C.green);
      nodeLabels['you'].setAttribute('fill', currentPath.length === 1 ? '#222' : '#fff');

      // Pulse celebrity if not yet reached
      if (currentPath.indexOf('celebrity') === -1) {
        nodeCircles['celebrity'].classList.add('gi-pulse');
        nodeCircles['celebrity'].setAttribute('fill', C.orange);
        nodeLabels['celebrity'].setAttribute('fill', '#fff');
      }
    }

    function handleNodeClick(id) {
      if (showingShortest) return;
      var last = currentPath[currentPath.length - 1];
      if (id === last) return;
      // Already in path?
      if (currentPath.indexOf(id) !== -1) return;

      var neighbours = adj(last);
      if (neighbours.indexOf(id) !== -1) {
        // Valid move
        currentPath.push(id);
        updateVisuals();
      } else {
        // Shake the node
        var circle = nodeCircles[id];
        var parent = circle.parentNode;
        parent.classList.add('gi-shake');
        setTimeout(function () { parent.classList.remove('gi-shake'); }, 350);
      }
    }

    btnShortest.addEventListener('click', function () {
      showingShortest = true;
      var sp = bfs('you', 'celebrity');
      if (!sp) return;

      // Reset visuals first
      currentPath = ['you'];
      updateVisuals();

      // Animate shortest path step by step
      sp.forEach(function (nid, idx) {
        setTimeout(function () {
          if (idx === 0) return;
          currentPath.push(nid);
          // Use yellow for shortest-path highlight
          for (var j = 0; j < currentPath.length; j++) {
            nodeCircles[currentPath[j]].setAttribute('fill', C.yellow);
            nodeLabels[currentPath[j]].setAttribute('fill', '#222');
            if (j > 0) {
              var key = [currentPath[j - 1], currentPath[j]].sort().join('--');
              if (edgeEls[key]) {
                edgeEls[key].setAttribute('stroke', C.yellow);
                edgeEls[key].setAttribute('stroke-width', 5);
                edgeEls[key].setAttribute('stroke-opacity', 1);
              }
            }
          }
          stepsText.textContent = 'Shortest: ' + (currentPath.length - 1) + ' steps';
        }, idx * 400);
      });
    });

    btnReset.addEventListener('click', function () {
      currentPath = ['you'];
      showingShortest = false;
      updateVisuals();
    });

    updateVisuals();
  }

  function resetSixDegrees() {
    sixDegreesInitialised = false;
    var c = document.getElementById('interactive-six-degrees');
    if (c) c.innerHTML = '';
  }

  // ===============================================================
  // 2. PAGERANK RANKING
  // ===============================================================
  var pageRankInitialised = false;

  function initPageRank() {
    var container = document.getElementById('interactive-pagerank');
    if (!container || pageRankInitialised) return;
    pageRankInitialised = true;
    container.innerHTML = '';

    // --- Data ---
    var prNodes = ['A', 'B', 'C', 'D', 'E'];
    var prEdges = [
      ['A','B'],['A','C'],['B','C'],['C','A'],
      ['D','C'],['E','C'],['E','D'],['B','E'],
    ];
    var ranks = {C: 0.34, A: 0.22, B: 0.18, E: 0.15, D: 0.11};
    var correctOrder = ['C', 'A', 'B', 'E', 'D'];

    var positions = {
      A: {x: 150, y: 150},
      B: {x: 350, y: 100},
      C: {x: 250, y: 300},
      D: {x: 100, y: 400},
      E: {x: 400, y: 350},
    };

    // --- Layout wrapper (flex row) ---
    var wrapper = htmlEl('div', {
      style: 'display:flex;gap:12px;align-items:flex-start;width:100%;',
    });
    container.appendChild(wrapper);

    // Left panel: SVG graph (60%)
    var leftPanel = htmlEl('div', {style: 'flex:0 0 60%;min-width:0;'});
    wrapper.appendChild(leftPanel);

    var svg = svgEl('svg', {
      viewBox: '0 0 500 480',
      width: '100%',
      style: 'display:block;max-height:360px;',
    });
    leftPanel.appendChild(svg);

    // Arrowhead marker
    var defs = svgEl('defs');
    var marker = svgEl('marker', {
      id: 'pr-arrow',
      viewBox: '0 0 10 10',
      refX: '28', refY: '5',
      markerWidth: '6', markerHeight: '6',
      orient: 'auto-start-reverse',
      fill: C.muted,
    });
    marker.appendChild(svgEl('path', {d: 'M0,0 L10,5 L0,10 z'}));
    defs.appendChild(marker);
    svg.appendChild(defs);

    // Edges (directed)
    var prEdgeEls = [];
    prEdges.forEach(function (e) {
      var a = positions[e[0]], b = positions[e[1]];
      var line = svgEl('line', {
        x1: a.x, y1: a.y, x2: b.x, y2: b.y,
        stroke: C.muted, 'stroke-width': 2,
        'marker-end': 'url(#pr-arrow)',
      });
      svg.appendChild(line);
      prEdgeEls.push({el: line, from: e[0], to: e[1]});
    });

    // Nodes
    var prNodeCircles = {};
    var baseRadius = 30;
    prNodes.forEach(function (id) {
      var p = positions[id];
      var g = svgEl('g');

      var circle = svgEl('circle', {
        cx: p.x, cy: p.y, r: baseRadius,
        fill: C.blue,
        stroke: 'rgba(255,255,255,.15)', 'stroke-width': 2,
        style: 'transition:r .6s ease,fill .3s;',
      });
      g.appendChild(circle);

      var txt = svgEl('text', {
        x: p.x, y: p.y + 6,
        fill: '#fff',
        'text-anchor': 'middle',
        'font-size': '18',
        'font-weight': '700',
        'pointer-events': 'none',
      });
      txt.textContent = id;
      g.appendChild(txt);

      svg.appendChild(g);
      prNodeCircles[id] = circle;
    });

    // Right panel: ranking slots + chips (40%)
    var rightPanel = htmlEl('div', {
      style: 'flex:0 0 38%;display:flex;flex-direction:column;align-items:center;',
    });
    wrapper.appendChild(rightPanel);

    var slotsTitle = htmlEl('div', {
      textContent: 'Rank the nodes by PageRank',
      style: 'color:' + C.text + ';font-size:14px;font-weight:700;margin-bottom:6px;',
    });
    rightPanel.appendChild(slotsTitle);

    // Slots
    var slotEls = [];
    var slotValues = [null, null, null, null, null]; // current assignment
    var slotsContainer = htmlEl('div', {style: 'width:100%;'});
    rightPanel.appendChild(slotsContainer);

    for (var i = 0; i < 5; i++) {
      (function (idx) {
        var slot = htmlEl('div', {class: 'pr-slot', 'data-index': idx});
        var label = htmlEl('span', {class: 'slot-label', textContent: 'Rank ' + (idx + 1)});
        var value = htmlEl('span', {class: 'slot-value', textContent: ''});
        slot.appendChild(label);
        slot.appendChild(value);
        slotsContainer.appendChild(slot);
        slotEls.push({el: slot, label: label, value: value});

        // Drop target
        slot.addEventListener('dragover', function (ev) { ev.preventDefault(); });
        slot.addEventListener('drop', function (ev) {
          ev.preventDefault();
          var nodeId = ev.dataTransfer.getData('text/plain');
          if (!nodeId) return;
          // Remove from any existing slot
          for (var s = 0; s < slotValues.length; s++) {
            if (slotValues[s] === nodeId) {
              slotValues[s] = null;
              slotEls[s].label.textContent = 'Rank ' + (s + 1);
              slotEls[s].el.classList.remove('filled');
            }
          }
          // Place in this slot (overwrite)
          if (slotValues[idx] !== null) {
            // Return existing chip
            var prev = slotValues[idx];
            chipMap[prev].classList.remove('placed');
          }
          slotValues[idx] = nodeId;
          slotEls[idx].label.textContent = 'Rank ' + (idx + 1) + ': ' + nodeId;
          slotEls[idx].el.classList.add('filled');
          chipMap[nodeId].classList.add('placed');
        });
      })(i);
    }

    // Chips
    var chipsRow = htmlEl('div', {
      style: 'display:flex;flex-wrap:wrap;justify-content:center;margin-top:12px;',
    });
    rightPanel.appendChild(chipsRow);

    var chipMap = {};
    prNodes.forEach(function (id) {
      var chip = htmlEl('div', {
        class: 'pr-chip',
        textContent: id,
        draggable: 'true',
      });
      chip.addEventListener('dragstart', function (ev) {
        ev.dataTransfer.setData('text/plain', id);
      });
      chipsRow.appendChild(chip);
      chipMap[id] = chip;
    });

    // Buttons
    var btnRow = htmlEl('div', {style: 'margin-top:10px;text-align:center;'});
    var btnCheck = htmlEl('button', {class: 'gi-btn gi-btn-green', textContent: 'Check Answer'});
    var btnPRReset = htmlEl('button', {class: 'gi-btn gi-btn-red', textContent: 'Reset'});
    btnRow.appendChild(btnCheck);
    btnRow.appendChild(btnPRReset);
    rightPanel.appendChild(btnRow);

    // --- Check logic ---
    btnCheck.addEventListener('click', function () {
      for (var idx = 0; idx < 5; idx++) {
        var placed = slotValues[idx];
        var slot = slotEls[idx];
        if (!placed) {
          slot.el.style.borderColor = C.muted;
          slot.value.textContent = '';
          continue;
        }
        var correctIdx = correctOrder.indexOf(placed);
        var off = Math.abs(idx - correctIdx);
        if (off === 0) {
          slot.el.style.borderColor = C.green;
          slot.el.style.background = 'rgba(46,204,113,.12)';
        } else if (off === 1) {
          slot.el.style.borderColor = C.orange;
          slot.el.style.background = 'rgba(230,126,34,.10)';
        } else {
          slot.el.style.borderColor = C.red;
          slot.el.style.background = 'rgba(231,76,60,.10)';
        }
        slot.value.textContent = placed + ': ' + Math.round(ranks[placed] * 100) + '%';
      }

      // Animate node sizes proportional to rank
      var maxRank = 0.34;
      prNodes.forEach(function (id) {
        var scale = 22 + (ranks[id] / maxRank) * 28; // range 22..50
        prNodeCircles[id].setAttribute('r', scale);
      });
    });

    btnPRReset.addEventListener('click', function () {
      slotValues = [null, null, null, null, null];
      slotEls.forEach(function (s, idx) {
        s.label.textContent = 'Rank ' + (idx + 1);
        s.value.textContent = '';
        s.el.style.borderColor = '';
        s.el.style.background = '';
        s.el.classList.remove('filled');
      });
      prNodes.forEach(function (id) {
        chipMap[id].classList.remove('placed');
        prNodeCircles[id].setAttribute('r', baseRadius);
      });
    });
  }

  function resetPageRank() {
    pageRankInitialised = false;
    var c = document.getElementById('interactive-pagerank');
    if (c) c.innerHTML = '';
  }

  // ===============================================================
  // 3. NETWORK ARCHITECTURE BUILDER
  // ===============================================================
  var architectInitialised = false;

  function initArchitect() {
    var container = document.getElementById('interactive-architect');
    if (!container || architectInitialised) return;
    architectInitialised = true;
    container.innerHTML = '';

    // --- Data ---
    var layers = {
      input:  [{id:'i0',x:100,y:100},{id:'i1',x:100,y:250},{id:'i2',x:100,y:400}],
      hidden: [{id:'h0',x:400,y:75},{id:'h1',x:400,y:200},{id:'h2',x:400,y:325},{id:'h3',x:400,y:450}],
      output: [{id:'o0',x:700,y:100},{id:'o1',x:700,y:250},{id:'o2',x:700,y:400}],
    };

    var allNodes = layers.input.concat(layers.hidden).concat(layers.output);
    var nodeById = {};
    allNodes.forEach(function (n) { nodeById[n.id] = n; });

    // Possible edges: any pair of distinct nodes among 10.
    // C(10,2) = 10*9/2 = 45 possible edges
    var possibleEdges = 45;

    // We allow edges between any two distinct nodes (user can click any pair).
    var drawnEdges = {}; // "id1--id2" (sorted) -> SVG line element
    var selectedNode = null;

    // --- SVG ---
    var svg = svgEl('svg', {
      viewBox: '0 0 800 500',
      width: '100%',
      height: '100%',
      style: 'display:block;max-height:380px;',
    });
    container.appendChild(svg);

    // Edges group
    var edgeGroup = svgEl('g');
    svg.appendChild(edgeGroup);

    // Column labels
    var labels = [
      {text: 'Input',  x: 100, y: 40},
      {text: 'Hidden', x: 400, y: 40},
      {text: 'Output', x: 700, y: 40},
    ];
    labels.forEach(function (l) {
      var t = svgEl('text', {
        x: l.x, y: l.y,
        fill: C.text,
        'text-anchor': 'middle',
        'font-size': '15',
        'font-weight': '700',
        'letter-spacing': '1',
        opacity: '0.7',
      });
      t.textContent = l.text;
      svg.appendChild(t);
    });

    // Nodes
    var nodeCircles = {};
    var nodeR = 28;

    function nodeColor(id) {
      if (id.charAt(0) === 'i') return C.green;
      if (id.charAt(0) === 'h') return C.blue;
      return C.orange;
    }

    allNodes.forEach(function (n) {
      var g = svgEl('g', {style: 'cursor:pointer'});

      var circle = svgEl('circle', {
        cx: n.x, cy: n.y, r: nodeR,
        fill: nodeColor(n.id),
        stroke: 'rgba(255,255,255,.15)', 'stroke-width': 2,
        style: 'transition:stroke .2s,stroke-width .2s;',
      });
      g.appendChild(circle);

      var label = svgEl('text', {
        x: n.x, y: n.y + 5,
        fill: '#fff',
        'text-anchor': 'middle',
        'font-size': '13',
        'font-weight': '700',
        'pointer-events': 'none',
      });
      // Short label: I1, H2, O3 etc.
      var prefix = n.id.charAt(0).toUpperCase();
      var num = parseInt(n.id.charAt(1), 10) + 1;
      label.textContent = prefix + num;
      g.appendChild(label);

      svg.appendChild(g);
      nodeCircles[n.id] = circle;

      g.addEventListener('click', function () { handleArchNodeClick(n.id); });
    });

    // Edge counter (top-right)
    var edgeCounter = svgEl('text', {
      x: 780, y: 30,
      fill: C.text,
      'text-anchor': 'end',
      'font-size': '15',
      'font-weight': '700',
    });
    edgeCounter.textContent = 'Edges: 0 / ' + possibleEdges + ' possible';
    svg.appendChild(edgeCounter);

    function updateCounter() {
      var n = Object.keys(drawnEdges).length;
      edgeCounter.textContent = 'Edges: ' + n + ' / ' + possibleEdges + ' possible';
    }

    function edgeKey(a, b) {
      return [a, b].sort().join('--');
    }

    function addEdge(a, b) {
      var key = edgeKey(a, b);
      if (drawnEdges[key]) return; // already exists
      var na = nodeById[a], nb = nodeById[b];
      var line = svgEl('line', {
        x1: na.x, y1: na.y, x2: nb.x, y2: nb.y,
        stroke: C.teal, 'stroke-width': 2.5, 'stroke-opacity': 0.7,
        style: 'cursor:pointer;',
      });
      line.addEventListener('click', function (ev) {
        ev.stopPropagation();
        removeEdge(key);
      });
      edgeGroup.appendChild(line);
      drawnEdges[key] = line;
      updateCounter();
    }

    function removeEdge(key) {
      if (!drawnEdges[key]) return;
      edgeGroup.removeChild(drawnEdges[key]);
      delete drawnEdges[key];
      updateCounter();
    }

    function clearSelection() {
      if (selectedNode) {
        nodeCircles[selectedNode].setAttribute('stroke', 'rgba(255,255,255,.15)');
        nodeCircles[selectedNode].setAttribute('stroke-width', '2');
        selectedNode = null;
      }
    }

    function handleArchNodeClick(id) {
      if (!selectedNode) {
        // Select first node
        selectedNode = id;
        nodeCircles[id].setAttribute('stroke', C.yellow);
        nodeCircles[id].setAttribute('stroke-width', '4');
      } else if (selectedNode === id) {
        // Deselect
        clearSelection();
      } else {
        // Second node: toggle edge
        var key = edgeKey(selectedNode, id);
        if (drawnEdges[key]) {
          removeEdge(key);
        } else {
          addEdge(selectedNode, id);
        }
        clearSelection();
      }
    }

    // Buttons + results area
    var controlRow = htmlEl('div', {style: 'text-align:center;margin-top:6px;'});
    var btnAnalyze = htmlEl('button', {class: 'gi-btn gi-btn-teal', textContent: 'Analyze'});
    var btnRandom  = htmlEl('button', {class: 'gi-btn gi-btn-blue', textContent: 'Random'});
    var btnArchReset = htmlEl('button', {class: 'gi-btn gi-btn-red', textContent: 'Reset'});
    controlRow.appendChild(btnAnalyze);
    controlRow.appendChild(btnRandom);
    controlRow.appendChild(btnArchReset);
    container.appendChild(controlRow);

    var resultsBox = htmlEl('div', {class: 'arch-results', style: 'display:none;'});
    container.appendChild(resultsBox);

    // --- Analysis ---
    function analyzeNetwork() {
      var edgeCount = Object.keys(drawnEdges).length;
      var density = edgeCount / possibleEdges;

      // Adjacency for BFS
      var adjMap = {};
      allNodes.forEach(function (n) { adjMap[n.id] = []; });
      Object.keys(drawnEdges).forEach(function (key) {
        var parts = key.split('--');
        adjMap[parts[0]].push(parts[1]);
        adjMap[parts[1]].push(parts[0]);
      });

      // Skip connections: any direct input->output edge
      var hasSkip = false;
      layers.input.forEach(function (inp) {
        layers.output.forEach(function (out) {
          if (drawnEdges[edgeKey(inp.id, out.id)]) hasSkip = true;
        });
      });

      // Fully connected: every output reachable from every input via BFS
      var fullyConnected = true;
      layers.input.forEach(function (inp) {
        layers.output.forEach(function (out) {
          if (!fullyConnected) return;
          // BFS from inp to out
          var visited = {};
          var queue = [inp.id];
          visited[inp.id] = true;
          var found = false;
          while (queue.length && !found) {
            var cur = queue.shift();
            if (cur === out.id) { found = true; break; }
            adjMap[cur].forEach(function (nb) {
              if (!visited[nb]) {
                visited[nb] = true;
                queue.push(nb);
              }
            });
          }
          if (!found) fullyConnected = false;
        });
      });

      // Classification
      var classification;
      if (!fullyConnected) {
        classification = 'Disconnected! -- some outputs have no input signal';
      } else if (density < 0.15) {
        classification = 'Sparse Feedforward -- efficient but limited';
      } else if (density <= 0.4 && !hasSkip) {
        classification = 'Standard Feedforward -- a classic workhorse';
      } else if (density <= 0.4 && hasSkip) {
        classification = 'ResNet-like -- shortcuts help learning!';
      } else if (density <= 0.7) {
        classification = 'Dense Network -- powerful but expensive';
      } else {
        classification = 'Transformer-like -- every node talks to every node!';
      }

      resultsBox.style.display = 'block';
      resultsBox.innerHTML = [
        '<strong>Density:</strong> ' + edgeCount + '/' + possibleEdges + ' = ' + Math.round(density * 100) + '%',
        '<strong>Skip connections:</strong> ' + (hasSkip ? 'Yes' : 'No'),
        '<strong>Fully connected:</strong> ' + (fullyConnected ? 'Yes' : 'No'),
        '<strong>Classification:</strong> ' + classification,
      ].join('<br>');
    }

    btnAnalyze.addEventListener('click', analyzeNetwork);

    btnRandom.addEventListener('click', function () {
      // Clear existing edges
      Object.keys(drawnEdges).forEach(function (key) {
        edgeGroup.removeChild(drawnEdges[key]);
      });
      drawnEdges = {};

      // Build list of valid pairs (all unique pairs of distinct nodes)
      var pairs = [];
      for (var i = 0; i < allNodes.length; i++) {
        for (var j = i + 1; j < allNodes.length; j++) {
          pairs.push([allNodes[i].id, allNodes[j].id]);
        }
      }

      // Shuffle and pick 10-25 random edges
      for (var k = pairs.length - 1; k > 0; k--) {
        var r = Math.floor(Math.random() * (k + 1));
        var tmp = pairs[k];
        pairs[k] = pairs[r];
        pairs[r] = tmp;
      }

      var count = 10 + Math.floor(Math.random() * 16); // 10..25
      for (var e = 0; e < count && e < pairs.length; e++) {
        addEdge(pairs[e][0], pairs[e][1]);
      }
      resultsBox.style.display = 'none';
      clearSelection();
    });

    btnArchReset.addEventListener('click', function () {
      Object.keys(drawnEdges).forEach(function (key) {
        edgeGroup.removeChild(drawnEdges[key]);
      });
      drawnEdges = {};
      updateCounter();
      resultsBox.style.display = 'none';
      clearSelection();
    });

    updateCounter();
  }

  function resetArchitect() {
    architectInitialised = false;
    var c = document.getElementById('interactive-architect');
    if (c) c.innerHTML = '';
  }

  // ===============================================================
  // Reveal.js integration
  // ===============================================================
  function slideContains(slide, id) {
    if (!slide) return false;
    return !!slide.querySelector('#' + id);
  }

  function onSlideChanged(event) {
    var current = event.currentSlide;
    var previous = event.previousSlide;

    // --- Six Degrees ---
    if (slideContains(current, 'interactive-six-degrees')) {
      initSixDegrees();
    }
    if (previous && slideContains(previous, 'interactive-six-degrees') &&
        !slideContains(current, 'interactive-six-degrees')) {
      resetSixDegrees();
    }

    // --- PageRank ---
    if (slideContains(current, 'interactive-pagerank')) {
      initPageRank();
    }
    if (previous && slideContains(previous, 'interactive-pagerank') &&
        !slideContains(current, 'interactive-pagerank')) {
      resetPageRank();
    }

    // --- Architect ---
    if (slideContains(current, 'interactive-architect')) {
      initArchitect();
    }
    if (previous && slideContains(previous, 'interactive-architect') &&
        !slideContains(current, 'interactive-architect')) {
      resetArchitect();
    }
  }

  // ---------------------------------------------------------------
  // Bootstrap
  // ---------------------------------------------------------------
  function boot() {
    injectStyles();

    // Wait for Reveal to be available and ready
    if (typeof Reveal !== 'undefined' && Reveal.isReady && Reveal.isReady()) {
      Reveal.on('slidechanged', onSlideChanged);
      // Init current slide immediately
      var current = Reveal.getCurrentSlide();
      if (current) {
        onSlideChanged({currentSlide: current, previousSlide: null});
      }
    } else if (typeof Reveal !== 'undefined' && Reveal.on) {
      // Reveal exists but may not be initialised yet
      Reveal.on('ready', function () {
        Reveal.on('slidechanged', onSlideChanged);
        var current = Reveal.getCurrentSlide();
        if (current) {
          onSlideChanged({currentSlide: current, previousSlide: null});
        }
      });
    } else {
      // Reveal not yet loaded; wait for DOMContentLoaded + poll
      var attempts = 0;
      var poll = setInterval(function () {
        attempts++;
        if (typeof Reveal !== 'undefined') {
          clearInterval(poll);
          if (Reveal.isReady && Reveal.isReady()) {
            Reveal.on('slidechanged', onSlideChanged);
            var current = Reveal.getCurrentSlide();
            if (current) {
              onSlideChanged({currentSlide: current, previousSlide: null});
            }
          } else if (Reveal.on) {
            Reveal.on('ready', function () {
              Reveal.on('slidechanged', onSlideChanged);
              var current = Reveal.getCurrentSlide();
              if (current) {
                onSlideChanged({currentSlide: current, previousSlide: null});
              }
            });
          }
        }
        if (attempts > 100) clearInterval(poll); // give up after ~10s
      }, 100);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();

// Page title block: "01 / 04" index + title rising out of a mask on the session entrance (spec row 9).
import { motion } from 'motion/react'
import { ease } from '../motion'

export function TitleBlock({ index, title, text, entrance: firstLoad, actions }) {
  return (
    <div className="title-block" style={{ display: 'flex', justifyContent: 'space-between', gap: 24, alignItems: 'flex-end', flexWrap: 'wrap' }}>
      <div>
        {index && <div className="title-index">{index} / 04</div>}
        <div className="title-mask">
          <motion.h1 initial={firstLoad ? { y: '100%' } : false} animate={{ y: 0 }}
            transition={{ duration: 0.7, delay: firstLoad ? 0.4 : 0, ease: ease.entrance }}>{title}</motion.h1>
        </div>
        {text && <p>{text}</p>}
      </div>
      {actions && <div className="row">{actions}</div>}
    </div>
  )
}
